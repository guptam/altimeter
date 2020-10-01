import unittest

from altimeter.core.resource.resource import Resource
from altimeter.aws.resource.ec2.route_table import EC2RouteTableResourceSpec


class TestRouteTableSchema(unittest.TestCase):
    def test_schema_parse(self):
        resource_arn = "arn:aws:ec2:us-east-2:111122223333:route-table/rtb-099c7b032f2bbddda"
        aws_resource_dict = {
            "Associations": [
                {
                    "Main": False,
                    "RouteTableAssociationId": "rtbassoc-069d59127bf10a728",
                    "RouteTableId": "rtb-099c7b032f2bbddda",
                    "SubnetId": "subnet-00f9fe55b9d7ca4fb",
                },
                {
                    "Main": False,
                    "RouteTableAssociationId": "rtbassoc-07bfd170c4ece33c8",
                    "RouteTableId": "rtb-099c7b032f2bbddda",
                    "SubnetId": "subnet-0b98092b454c882cf",
                },
            ],
            "PropagatingVgws": [],
            "RouteTableId": "rtb-099c7b032f2bbddda",
            "Routes": [
                {
                    "DestinationCidrBlock": "172.31.0.0/16",
                    "GatewayId": "local",
                    "Origin": "CreateRouteTable",
                    "State": "active",
                },
                {
                    "DestinationCidrBlock": "0.0.0.0/0",
                    "GatewayId": "igw-092e5ec1685fd0c0b",
                    "Origin": "CreateRoute",
                    "State": "active",
                },
                {
                    "DestinationPrefixListId": "pl-68a54001",
                    "GatewayId": "vpce-0678bce2b63b8ad0f",
                    "Origin": "CreateRoute",
                    "State": "active",
                },
            ],
            "VpcId": "vpc-03c33051f57d21ff0",
            "OwnerId": "210554966933",
        }

        links = EC2RouteTableResourceSpec.schema.parse(
            data=aws_resource_dict, context={"account_id": "111122223333", "region": "us-west-2"}
        )
        resource = Resource(
            resource_id=resource_arn, resource_type=EC2RouteTableResourceSpec.type_name, links=links
        )
        alti_resource_dict = resource.dict()

        expected_alti_resource_dict = {
            "resource_id": "arn:aws:ec2:us-east-2:111122223333:route-table/rtb-099c7b032f2bbddda",
            "resource_type": "route-table",
            "links": [
                {"pred": "route_table_id", "obj": "rtb-099c7b032f2bbddda", "link_type": "simple"},
                {
                    "pred": "vpc",
                    "obj": "arn:aws:ec2:us-west-2:111122223333:vpc/vpc-03c33051f57d21ff0",
                    "link_type": "resource_link",
                },
                {"pred": "owner_id", "obj": "210554966933", "link_type": "simple"},
                {
                    "pred": "route",
                    "obj": [
                        {
                            "pred": "destination_cidr_block",
                            "obj": "172.31.0.0/16",
                            "link_type": "simple",
                        },
                        {"pred": "gateway_id", "obj": "local", "link_type": "simple"},
                        {"pred": "origin", "obj": "CreateRouteTable", "link_type": "simple"},
                        {"pred": "state", "obj": "active", "link_type": "simple"},
                    ],
                    "link_type": "multi",
                },
                {
                    "pred": "route",
                    "obj": [
                        {"pred": "destination_cidr_block", "obj": "0.0.0.0/0", "link_type": "simple"},
                        {"pred": "gateway_id", "obj": "igw-092e5ec1685fd0c0b", "link_type": "simple"},
                        {"pred": "origin", "obj": "CreateRoute", "link_type": "simple"},
                        {"pred": "state", "obj": "active", "link_type": "simple"},
                    ],
                    "link_type": "multi",
                },
                {
                    "pred": "route",
                    "obj": [
                        {
                            "pred": "destination_prefix_list_id",
                            "obj": "pl-68a54001",
                            "link_type": "simple",
                        },
                        {"pred": "gateway_id", "obj": "vpce-0678bce2b63b8ad0f", "link_type": "simple"},
                        {"pred": "origin", "obj": "CreateRoute", "link_type": "simple"},
                        {"pred": "state", "obj": "active", "link_type": "simple"},
                    ],
                    "link_type": "multi",
                },
                {
                    "pred": "association",
                    "obj": [
                        {"pred": "main", "obj": False, "link_type": "simple"},
                        {
                            "pred": "route_table_association_id",
                            "obj": "rtbassoc-069d59127bf10a728",
                            "link_type": "simple",
                        },
                        {
                            "pred": "route_table_id",
                            "obj": "rtb-099c7b032f2bbddda",
                            "link_type": "simple",
                        },
                        {"pred": "subnet_id", "obj": "subnet-00f9fe55b9d7ca4fb", "link_type": "simple"},
                    ],
                    "link_type": "multi",
                },
                {
                    "pred": "association",
                    "obj": [
                        {"pred": "main", "obj": False, "link_type": "simple"},
                        {
                            "pred": "route_table_association_id",
                            "obj": "rtbassoc-07bfd170c4ece33c8",
                            "link_type": "simple",
                        },
                        {
                            "pred": "route_table_id",
                            "obj": "rtb-099c7b032f2bbddda",
                            "link_type": "simple",
                        },
                        {"pred": "subnet_id", "obj": "subnet-0b98092b454c882cf", "link_type": "simple"},
                    ],
                    "link_type": "multi",
                },
            ],
        }
        self.assertDictEqual(alti_resource_dict, expected_alti_resource_dict)
