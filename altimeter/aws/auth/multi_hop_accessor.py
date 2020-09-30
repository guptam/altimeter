"""A MultiHopAccessor contains a list of AccessSteps defining how to gain access to an account via
role assumption(s)."""
import os
from typing import List, Optional

import boto3
import jinja2
from pydantic import validator

from altimeter.aws.auth.cache import AWSCredentials, AWSCredentialsCache
from altimeter.core.log import Logger
from altimeter.core.log_events import LogEvent
from altimeter.core.alti_base_model import BaseAltiModel


class AccessStep(BaseAltiModel):
    """Represents a single access step to get to an account.

    Args:
        role_name: role name for this step
        account_id: account_id for this step. If empty this step is assumed to be the last
                    in a chain of multiple AccessSteps
        external_id: external_id to use for access (if needed).
    """

    role_name: str
    account_id: Optional[str]
    external_id: Optional[str]

    @validator("external_id")
    # pylint: disable=no-self-argument,no-self-use
    def interpolate_ext_id(cls, val: Optional[str]) -> Optional[str]:
        """Interpolate an external id from an env var using jinja2"""
        if val is not None:
            template = jinja2.Environment(
                loader=jinja2.BaseLoader(),
                undefined=jinja2.StrictUndefined,
                autoescape=jinja2.select_autoescape(
                    enabled_extensions=("html", "xml"), default_for_string=True
                ),
            ).from_string(val)
            return template.render(env=os.environ)
        return None

    def __str__(self) -> str:
        account = self.account_id if self.account_id else "target"
        return f"{self.role_name}@{account}"


class MultiHopAccessor(BaseAltiModel):
    """A MultiHopAccessor contains a list of AccessSteps defining how to gain access to an account
    via role assumption(s).

    Args:
        role_session_name: role session name to use for session creation.
        access_steps: list of AccessSteps defining how to access a final
                      destination account.
    """

    role_session_name: str
    access_steps: List[AccessStep]

    @validator("access_steps")
    # pylint: disable=no-self-argument,no-self-use
    def validate_access_steps(cls, val: List[AccessStep]) -> List[AccessStep]:
        """Validate that the access steps of this MHA are valid"""
        if not val:
            raise ValueError("MultiHopAccessor must have a non-empty list of AccessSteps")
        for access_step in val[:-1]:
            if not access_step.account_id:
                raise ValueError(
                    "Non-final AccessStep of a MultiHopAccessor must specify an account_id"
                )
        if val[-1].account_id:
            raise ValueError(
                "The last AccessStep of a MultiHopAccessor must not specify account_id"
            )
        return val

    def get_session(
        self,
        account_id: str,
        region_name: Optional[str] = None,
        credentials_cache: Optional[AWSCredentialsCache] = None,
    ) -> boto3.Session:
        """Get a session for an account_id by iterating through the :class:`.AccessStep`s
        of this :class:`.MultiHopAccessor`.

        Args:
             account_id: account to access
             region_name: region to use during session creation.

        Returns:
            boto3 Session for accessing account_id
        """
        logger = Logger()
        cws = boto3.Session(region_name=region_name)
        for access_step in self.access_steps:
            access_account_id = access_step.account_id if access_step.account_id else account_id
            role_name = access_step.role_name
            external_id = access_step.external_id
            session = None
            if credentials_cache is not None:
                session = credentials_cache.get(
                    account_id=access_account_id,
                    role_name=role_name,
                    role_session_name=self.role_session_name,
                    region_name=region_name,
                )
            if session is None:
                logger.debug(event=LogEvent.AuthToAccountStart)
                sts_client = cws.client("sts")
                role_arn = f"arn:aws:iam::{access_account_id}:role/{role_name}"
                assume_args = {"RoleArn": role_arn, "RoleSessionName": self.role_session_name}
                if external_id:
                    assume_args["ExternalId"] = external_id

                assume_resp = sts_client.assume_role(**assume_args)
                creds = assume_resp["Credentials"]
                expiration_datetime = creds["Expiration"]
                credentials = AWSCredentials(
                    access_key_id=creds["AccessKeyId"],
                    secret_access_key=creds["SecretAccessKey"],
                    session_token=creds["SessionToken"],
                    expiration=int(expiration_datetime.timestamp()),
                )
                session = boto3.Session(
                    aws_access_key_id=creds["AccessKeyId"],
                    aws_secret_access_key=creds["SecretAccessKey"],
                    aws_session_token=creds["SessionToken"],
                    region_name=region_name,
                )
                if credentials_cache is not None:
                    credentials_cache.put(
                        credentials=credentials,
                        account_id=access_account_id,
                        role_name=role_name,
                        role_session_name=self.role_session_name,
                    )
                logger.debug(event=LogEvent.AuthToAccountEnd)
            cws = session
        return session

    def __str__(self) -> str:
        return f'accessor:{self.role_session_name}:{",".join([str(access_step) for access_step in self.access_steps])}'
