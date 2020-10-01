import unittest

from altimeter.core.resource.resource import Resource
from altimeter.aws.resource.iam.account_password_policy import IAMAccountPasswordPolicyResourceSpec


class TestAccountPasswordPolicyResourceSpec(unittest.TestCase):
    def test_schema_parse(self):
        resource_arn = "arn:aws:iam:us-west-2:111122223333:account-password-policy/default"
        aws_resource_dict = {
            'MinimumPasswordLength': 12, 'RequireSymbols': True, 'RequireNumbers': True,
            'RequireUppercaseCharacters': True, 'RequireLowercaseCharacters': True, 'AllowUsersToChangePassword': True,
            'ExpirePasswords': True, 'MaxPasswordAge': 90, 'PasswordReusePrevention': 5, 'HardExpiry': True
        }

        links = IAMAccountPasswordPolicyResourceSpec.schema.parse(
            data=aws_resource_dict, context={"account_id": "111122223333", "region": "us-west-2"}
        )
        resource = Resource(
            resource_id=resource_arn, resource_type=IAMAccountPasswordPolicyResourceSpec.type_name, links=links
        )
        alti_resource_dict = resource.dict()

        expected_alti_resource_dict = {'resource_id': 'arn:aws:iam:us-west-2:111122223333:account-password-policy/default',
                                       'resource_type': 'account-password-policy',
                                       'links': [{'pred': 'minimum_password_length', 'obj': 12, 'field_type': 'simple'},
                                                 {'pred': 'require_symbols', 'obj': True, 'field_type': 'simple'},
                                                 {'pred': 'require_numbers', 'obj': True, 'field_type': 'simple'}, {
                                                     'pred': 'require_uppercase_characters', 'obj': True,
                                                     'field_type': 'simple'
                                                 }, {
                                                     'pred': 'require_lowercase_characters', 'obj': True,
                                                     'field_type': 'simple'
                                                 }, {
                                                     'pred': 'allow_users_to_change_password', 'obj': True,
                                                     'field_type': 'simple'
                                                 }, {'pred': 'expire_passwords', 'obj': True, 'field_type': 'simple'},
                                                 {'pred': 'max_password_age', 'obj': 90, 'field_type': 'simple'},
                                                 {'pred': 'password_reuse_prevention', 'obj': 5, 'field_type': 'simple'},
                                                 {'pred': 'hard_expiry', 'obj': True, 'field_type': 'simple'}]
        }

        self.assertDictEqual(alti_resource_dict, expected_alti_resource_dict)
