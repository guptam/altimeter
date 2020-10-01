from unittest import TestCase

import boto3
from moto import mock_ec2

from altimeter.aws.resource.ec2.volume import EBSVolumeResourceSpec
from altimeter.aws.scan.aws_accessor import AWSAccessor


class TestEBSVolumeResourceSpec(TestCase):
    @mock_ec2
    def test_scan(self):
        account_id = "123456789012"
        region_name = "us-east-1"

        session = boto3.Session()

        ec2_client = session.client("ec2", region_name=region_name)
        resp = ec2_client.create_volume(Size=1, AvailabilityZone="us-east-1a")
        create_time = resp["CreateTime"]
        volume_id = resp["VolumeId"]
        volume_arn = f"arn:aws:ec2:us-east-1:123456789012:volume/{volume_id}"

        scan_accessor = AWSAccessor(session=session, account_id=account_id, region_name=region_name)
        resources = EBSVolumeResourceSpec.scan(scan_accessor=scan_accessor)

        expected_resources = [
            {
                "resource_id": volume_arn,
                "resource_type": "aws:ec2:volume",
                "links": [
                    {"pred": "availability_zone", "obj": "us-east-1a", "link_type": "simple"},
                    {"pred": "create_time", "obj": create_time, "link_type": "simple"},
                    {"pred": "size", "obj": 1, "link_type": "simple"},
                    {"pred": "state", "obj": "available", "link_type": "simple"},
                    {"pred": "volume_type", "obj": "standard", "link_type": "simple"},
                    {"pred": "encrypted", "obj": False, "link_type": "simple"},
                    {
                        "pred": "account",
                        "obj": "arn:aws::::account/123456789012",
                        "link_type": "resource_link",
                    },
                    {
                        "pred": "region",
                        "obj": "arn:aws:::123456789012:region/us-east-1",
                        "link_type": "resource_link",
                    },
                ],
            }
        ]

        expected_api_call_stats = {
            "count": 1,
            "123456789012": {
                "count": 1,
                "us-east-1": {"count": 1, "ec2": {"count": 1, "DescribeVolumes": {"count": 1}}},
            },
        }
        self.assertListEqual([resource.dict() for resource in resources], expected_resources)
        self.assertDictEqual(scan_accessor.api_call_stats.to_dict(), expected_api_call_stats)
