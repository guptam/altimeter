"""Configuration classes"""
from pathlib import Path
from typing import Any, Dict, Optional, Type, Tuple

import boto3
from pydantic import Field, root_validator, validator, ValidationError
import toml

from altimeter.aws.auth.accessor import Accessor
from altimeter.core.artifact_io import is_s3_uri, parse_s3_uri
from altimeter.core.alti_base_model import BaseAltiModel


class InvalidConfigException(Exception):
    """Indicates an invalid configuration"""


class ScanConfig(BaseAltiModel):
    """Scan configuration class"""

    accounts: Tuple[str, ...]
    regions: Tuple[str, ...]
    scan_sub_accounts: bool = False
    preferred_account_scan_regions: Tuple[str, ...]
    scan_lambda_tcp_keepalive: bool = False


class ConcurrencyConfig(BaseAltiModel):
    """Concurrency configuration class"""

    max_account_scan_threads: int
    max_accounts_per_thread: int
    max_svc_scan_threads: int


class NeptuneConfig(BaseAltiModel):
    """Neptune configuration class"""

    host: str
    port: int
    region: str
    iam_role_arn: Optional[str]
    graph_load_sns_topic_arn: Optional[str]
    ssl: bool = True
    use_lpg: bool = False
    iam_credentials_provider_type: Optional[str]
    auth_mode: Optional[str]


class Config(BaseAltiModel):
    """Top level configuration class"""

    artifact_path: str
    pruner_max_age_min: int
    graph_name: str
    concurrency: ConcurrencyConfig
    scan: ScanConfig
    accessor: Accessor = Field(default_factory=Accessor)
    neptune: Optional[NeptuneConfig] = None

    @validator("artifact_path")
    # pylint: disable=no-self-argument,no-self-use
    def validate_s3_artifact_path(cls, val: str) -> str:
        """Validate that if artifact_path looks like an s3 uri, it is valid"""
        if is_s3_uri(val):
            _, key_prefix = parse_s3_uri(val)
            if key_prefix is not None:
                raise InvalidConfigException(
                    f"S3 artifact_path should be s3://<bucket>, no key - got {val}"
                )
        return val

    @root_validator
    # pylint: disable=no-self-argument,no-self-use
    def no_multi_hop_accessors_for_single_account(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that if single account scan is configured, no multihop accessors
        are configured"""
        if not values["scan"].accounts:
            if not values["scan"].scan_sub_accounts:
                if values.get("accessor", Accessor()).multi_hop_accessors:
                    raise InvalidConfigException(
                        "Accessor config not supported for single account mode without "
                        "scan_sub_accounts"
                    )
        return values

    @root_validator
    # pylint: disable=no-self-argument,no-self-use
    def multi_hop_accessors_required_for_scan_sub_accounts(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate that if scan_sub_accounts is True, multihop accessors are configured"""
        if values["scan"].scan_sub_accounts:
            if not values.get("accessor", Accessor()).multi_hop_accessors:
                raise InvalidConfigException("Accessor config required for scan_sub_accounts")
        return values

    @classmethod
    def from_path(cls: Type["Config"], path: str) -> "Config":
        """Load a Config from an s3 uri or a  file"""
        if is_s3_uri(path):
            return cls.from_s3(s3_uri=path)
        return cls.from_file(filepath=Path(path))

    @classmethod
    def from_file(cls: Type["Config"], filepath: Path) -> "Config":
        """Load a Config from a file"""
        with open(filepath, "r") as fp:
            config_str = fp.read()
        config_dict = dict(toml.loads(config_str))
        try:
            return cls.parse_obj(config_dict)
        except ValidationError as ve:
            raise InvalidConfigException(f"Error in conf file {filepath}: {str(ve)}") from ve

    @classmethod
    def from_s3(cls: Type["Config"], s3_uri: str) -> "Config":
        """Load a Config from an s3 object"""
        bucket, key = parse_s3_uri(s3_uri)
        s3_client = boto3.client("s3")
        resp = s3_client.get_object(Bucket=bucket, Key=key,)
        config_str = resp["Body"].read().decode("utf-8")
        config_dict = dict(toml.loads(config_str))
        try:
            return cls.parse_obj(config_dict)
        except ValidationError as ve:
            raise InvalidConfigException(f"Error in conf file {s3_uri}: {str(ve)}") from ve
