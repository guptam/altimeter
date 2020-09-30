from unittest import TestCase

from altimeter.core.config import Config, ScanConfig


class TestScanConfig(TestCase):
    def test_from_dict(self):
        scan_config_dict = {
            "accounts": ["123", "456"],
            "regions": ["us-west-2", "us-west-1"],
            "scan_sub_accounts": False,
            "preferred_account_scan_regions": ["us-east-1", "us-west-2"],
        }
        scan_config = ScanConfig.parse_obj(scan_config_dict)
        self.assertTupleEqual(scan_config.accounts, ("123", "456"))
        self.assertTupleEqual(scan_config.regions, ("us-west-2", "us-west-1"))
        self.assertEqual(scan_config.scan_sub_accounts, False)
        self.assertTupleEqual(scan_config.preferred_account_scan_regions, ("us-east-1", "us-west-2"))

class TestSampleConfigs(TestCase):
    def test_single_account(self):
        Config.from_file("conf/single_account.toml")

    def test_current_single_account(self):
        Config.from_file("conf/current_single_account.toml")

    def test_current_master_multi_account(self):
        Config.from_file("conf/current_master_multi_account.toml")

class TestConfig(TestCase):
    def test_from_dict(self):
        config_dict = {
            'artifact_path': '/tmp/altimeter_single_account',
            'pruner_max_age_min': 4320,
            'graph_name': 'alti',
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
            },
            'neptune': None
        }
        config = Config.parse_obj(config_dict)
        self.assertIsNone(config.neptune)
        self.assertEqual(config.pruner_max_age_min, 4320)

