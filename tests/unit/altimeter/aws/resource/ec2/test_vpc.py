from unittest import TestCase

import boto3
from moto import mock_ec2

from altimeter.aws.resource.ec2.vpc import VPCResourceSpec
from altimeter.aws.scan.aws_accessor import AWSAccessor


class TestVPCResourceSpec(TestCase):
    @mock_ec2
    def test_scan(self):
        account_id = "123456789012"
        region_name = "us-east-1"

        session = boto3.Session()

        ec2_client = session.client("ec2", region_name=region_name)

        # find the moto vpc id, it's random
        list_resp = ec2_client.describe_vpcs()
        moto_vpcs = list_resp["Vpcs"]
        self.assertEqual(len(moto_vpcs), 1)
        moto_vpc_id = moto_vpcs[0]["VpcId"]
        moto_vpc_arn = f"arn:aws:ec2:us-east-1:123456789012:vpc/{moto_vpc_id}"


        vpc_resp = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
        vpc_id = vpc_resp["Vpc"]["VpcId"]
        vpc_arn = f"arn:aws:ec2:us-east-1:123456789012:vpc/{vpc_id}"

        scan_accessor = AWSAccessor(session=session, account_id=account_id, region_name=region_name)
        resources = VPCResourceSpec.scan(scan_accessor=scan_accessor)

        expected_resources = [
            {
                "resource_id": moto_vpc_arn,
                "resource_type": "aws:ec2:vpc",
                "links": [
                    {"pred": "is_default", "obj": True, "link_type": "simple"},
                    {
                        "pred": "cidr_block",
                        "obj": "172.31.0.0/16",
                        "link_type": "simple",
                    },  # from moto
                    {"pred": "state", "obj": "available", "link_type": "simple"},
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
            },
            {
                "resource_id": vpc_arn,
                "resource_type": "aws:ec2:vpc",
                "links": [
                    {"pred": "is_default", "obj": False, "link_type": "simple"},
                    {"pred": "cidr_block", "obj": "10.0.0.0/16", "link_type": "simple"},
                    {"pred": "state", "obj": "available", "link_type": "simple"},
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
            },
        ]
        expected_api_call_stats = {
            "count": 1,
            "123456789012": {
                "count": 1,
                "us-east-1": {"count": 1, "ec2": {"count": 1, "DescribeVpcs": {"count": 1}}},
            },
        }
        self.maxDiff = None
        self.assertListEqual([resource.dict() for resource in resources], expected_resources)
        self.assertDictEqual(scan_accessor.api_call_stats.to_dict(), expected_api_call_stats)
