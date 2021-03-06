from unittest import TestCase

from altimeter.core.config import (
    Config,
    InvalidConfigException,
    get_optional_section,
    get_required_list_param,
    get_required_bool_param,
    get_required_int_param,
    get_required_section,
    get_required_str_param,
    ScanConfig,
)

class TestGetRequiredListParam(TestCase):
    def test_present(self):
        config_dict = {"foo": ["ab", "cd"]}
        value = get_required_list_param("foo", config_dict)
        self.assertEqual(value, ("ab", "cd"))

    def test_absent(self):
        config_dict = {"abcd": "foo"}
        with self.assertRaises(InvalidConfigException):
            get_required_list_param("foo", config_dict)

    def test_nonlist(self):
        config_dict = {"foo": "abcd"}
        with self.assertRaises(InvalidConfigException):
            get_required_list_param("foo", config_dict)

class TestGetRequiredBoolParam(TestCase):
    def test_present(self):
        config_dict = {"foo": True}
        value = get_required_bool_param("foo", config_dict)
        self.assertEqual(value, True)

    def test_absent(self):
        config_dict = {"abcd": True}
        with self.assertRaises(InvalidConfigException):
            get_required_bool_param("foo", config_dict)

    def test_nonbool(self):
        config_dict = {"foo": "abcd"}
        with self.assertRaises(InvalidConfigException):
            get_required_bool_param("foo", config_dict)

class TestGetRequiredIntParam(TestCase):
    def test_present(self):
        config_dict = {"foo": 1}
        value = get_required_int_param("foo", config_dict)
        self.assertEqual(value, 1)

    def test_absent(self):
        config_dict = {"abcd": 1}
        with self.assertRaises(InvalidConfigException):
            get_required_int_param("foo", config_dict)

    def test_nonint(self):
        config_dict = {"foo": "abcd"}
        with self.assertRaises(InvalidConfigException):
            get_required_int_param("foo", config_dict)

class TestGetRequiredStrParam(TestCase):
    def test_present(self):
        config_dict = {"foo": "abcd"}
        value = get_required_str_param("foo", config_dict)
        self.assertEqual(value, "abcd")

    def test_absent(self):
        config_dict = {"abcd": "foo"}
        with self.assertRaises(InvalidConfigException):
            get_required_str_param("foo", config_dict)

    def test_nonstr(self):
        config_dict = {"foo": 1}
        with self.assertRaises(InvalidConfigException):
            get_required_str_param("foo", config_dict)

class TestGetRequiredSection(TestCase):
    def test_present(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        section = get_required_section("SectionA", config_dict)
        self.assertDictEqual(section, {"foo": "boo"})

    def test_absent(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        with self.assertRaises(InvalidConfigException):
            get_required_section("SectionB", config_dict)

    def test_nondict(self):
        config_dict = {"SectionA": "foo"}
        with self.assertRaises(InvalidConfigException):
            get_required_section("SectionA", config_dict)

class TestGetRequiredSection(TestCase):
    def test_present(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        section = get_required_section("SectionA", config_dict)
        self.assertDictEqual(section, {"foo": "boo"})

    def test_absent(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        with self.assertRaises(InvalidConfigException):
            get_required_section("SectionB", config_dict)

    def test_nondict(self):
        config_dict = {"SectionA": "foo"}
        with self.assertRaises(InvalidConfigException):
            get_required_section("SectionA", config_dict)

class TestGetOptionalSection(TestCase):
    def test_present(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        section = get_optional_section("SectionA", config_dict)
        self.assertDictEqual(section, {"foo": "boo"})

    def test_absent(self):
        config_dict = {"SectionA": {"foo": "boo"}}
        section = get_optional_section("SectionB", config_dict)
        self.assertIsNone(section)

    def test_nondict(self):
        config_dict = {"SectionA": "foo"}
        with self.assertRaises(InvalidConfigException):
            get_optional_section("SectionA", config_dict)

class TestScanConfig(TestCase):
    def test_from_dict(self):
        scan_config_dict = {
            "accounts": ["123", "456"],
            "regions": ["us-west-2", "us-west-1"],
            "scan_sub_accounts": False,
            "preferred_account_scan_regions": ["us-east-1", "us-west-2"],
            "single_account_mode": False,
        }
        scan_config = ScanConfig.from_dict(scan_config_dict)
        self.assertTupleEqual(scan_config.accounts, ("123", "456"))
        self.assertTupleEqual(scan_config.regions, ("us-west-2", "us-west-1"))
        self.assertEqual(scan_config.scan_sub_accounts, False)
        self.assertTupleEqual(scan_config.preferred_account_scan_regions, ("us-east-1", "us-west-2"))
        self.assertEqual(scan_config.single_account_mode, False)
        config = Config.from_file("conf/single_account.toml")

class TestConfig(TestCase):
    def test_from_dict(self):
        config_dict = {
            'artifact_path': '/tmp/altimeter_single_account',
            'pruner_max_age_min': 4320,
            'graph_name': 'alti',
            'access': {
                'accessor': {
                    'multi_hop_accessors': [],
                    'credentials_cache': {
                        'cache': {}
                    }
                }
            },
            'concurrency': {
                'max_account_scan_threads': 1,
                'max_accounts_per_thread': 1,
                'max_svc_scan_threads': 64
            },
            'scan': {
                'accounts': ('1234',),
                'regions': (),
                'scan_sub_accounts': False,
                'preferred_account_scan_regions': (
                    'us-west-1',
                    'us-west-2',
                    'us-east-1',
                    'us-east-2'
                ),
                'single_account_mode': False
            },
            'neptune': None
        }
        config = Config.from_dict(config_dict)
        self.assertIsNone(config.neptune)
        self.assertEqual(config.pruner_max_age_min, 4320)

