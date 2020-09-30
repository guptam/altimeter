import datetime
import unittest

from dateutil.tz import tzutc

from altimeter.aws.resource.ec2.transit_gateway_vpc_attachment import (
    TransitGatewayVpcAttachmentResourceSpec,
)
from altimeter.core.resource.resource import Resource


class TestTransitGatewayVpcAttachmentSchema(unittest.TestCase):
    def test_schema_parse(self):
        self.maxDiff = None
        resource_arn = "arn:aws:ec2:us-east-2:111122223333:transit-gateway-vpc-attachment/tgw-attach-09ece7878ee9ab7a4"
        aws_resource_dict = {
            "TransitGatewayAttachmentId": "tgw-attach-09ece7878ee9ab7a4",
            "TransitGatewayId": "tgw-086b599bebfee5d40",
            "VpcId": "vpc-01e8457e8c00c40a7",
            "VpcOwnerId": "123456789012",
            "State": "available",
            "SubnetIds": ["subnet-07697f82fe4c6a8d6", "subnet-0396137c18d6c30ef"],
            "CreationTime": datetime.datetime(2019, 8, 23, 15, 59, 46, tzinfo=tzutc()),
            "Options": {"DnsSupport": "enable", "Ipv6Support": "disable"},
            "Tags": [{"Key": "Name", "Value": "customer-dev-tgw-attachment"}],
        }

        links = TransitGatewayVpcAttachmentResourceSpec.schema.parse(
            data=aws_resource_dict, context={"account_id": "111122223333", "region": "us-west-2"}
        )
        resource = Resource(
            resource_id=resource_arn,
            type_name=TransitGatewayVpcAttachmentResourceSpec.type_name,
            links=links,
        )
        alti_resource_dict = resource.to_dict()

        expected_alti_resource_dict = {
            "type": "transit-gateway-vpc-attachment",
            "links": [
                {
                    "pred": "transit_gateway_attachment_id",
                    "obj": "tgw-attach-09ece7878ee9ab7a4",
                    "field_type": "simple",
                },
                {"pred": "transit_gateway_id", "obj": "tgw-086b599bebfee5d40", "field_type": "simple"},
                {"pred": "vpc_id", "obj": "vpc-01e8457e8c00c40a7", "field_type": "simple"},
                {"pred": "vpc_owner_id", "obj": "123456789012", "field_type": "simple"},
                {"pred": "state", "obj": "available", "field_type": "simple"},
                {
                    "pred": "creation_time",
                    "obj": datetime.datetime(2019, 8, 23, 15, 59, 46, tzinfo=tzutc()),
                    "field_type": "simple",
                },
                {"obj": "subnet-07697f82fe4c6a8d6",
                    "pred": "subnet_id",
                    "field_type": "simple"
                },
                {"obj": "subnet-0396137c18d6c30ef",
                    "pred": "subnet_id",
                    "field_type": "simple"
                },
                {"pred": "dns_support", "obj": "enable", "field_type": "simple"},
                {"pred": "ipv6_support", "obj": "disable", "field_type": "simple"},
            ],
        }
        self.assertDictEqual(alti_resource_dict, expected_alti_resource_dict)
