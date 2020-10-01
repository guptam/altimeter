from unittest import TestCase

import boto3
from moto import mock_sts

from altimeter.aws.resource.account import AccountResourceSpec
from altimeter.aws.scan.aws_accessor import AWSAccessor


class TestEBSVolumeResourceSpec(TestCase):
    @mock_sts
    def test_scan(self):
        account_id = "123456789012"
        region_name = "us-east-1"

        session = boto3.Session()
        scan_accessor = AWSAccessor(session=session, account_id=account_id, region_name=region_name)
        resources = AccountResourceSpec.scan(scan_accessor=scan_accessor)

        expected_resources = [
            {
                "resource_id": "arn:aws::::account/123456789012",
                "resource_type": "aws:account",
                "links": [{"pred": "account_id", "obj": "123456789012", "field_type": "simple"}],
            }
        ]
        expected_api_call_stats = {
            "count": 1,
            "123456789012": {
                "count": 1,
                "us-east-1": {
                    "count": 1,
                    "sts": {"count": 1, "GetCallerIdentity": {"count": 1}},
                },
            },
        }
        self.assertListEqual([resource.dict() for resource in resources], expected_resources)
        self.assertDictEqual(scan_accessor.api_call_stats.to_dict(), expected_api_call_stats)

    @mock_sts
    def test_detect_account_id_session_mismatch(self):
        account_id = "234567890121"
        region_name = "us-east-1"

        session = boto3.Session()
        scan_accessor = AWSAccessor(session=session, account_id=account_id, region_name=region_name)
        with self.assertRaises(ValueError):
            AccountResourceSpec.scan(scan_accessor=scan_accessor)

    def test_generate_arn(self):
        account_id = "234567890121"
        region_name = "us-east-1"
        resource_id = "123456789012"

        expected_arn = "arn:aws::::account/123456789012"
        arn = AccountResourceSpec.generate_arn(
            account_id=account_id, region=region_name, resource_id=resource_id
        )
        self.assertEqual(arn, expected_arn)
