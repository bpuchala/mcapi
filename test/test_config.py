import unittest
from mcapi import Config

class TestConfigProject(unittest.TestCase):

    def setup(self):
        test_data_dir = "test/test_config_data/"
        if (not exists(test_data_dir)):
            Exception("No test data for TestRemote. Can not find directory: " + test_data_dir);

    def test_default_config(self):
        config = Config()
        self.assertIsNotNone(config)
        self.assertIsNotNone(config.params)
        self.assertIsNotNone(config.params['apikey'])
        self.assertIsNotNone(config.mcurl)

    def test_path_settings(self):
        config = Config(config_file_path="test/test_config_data/", config_file_name="config.json")
        self.assertIsNotNone(config)
        self.assertIsNotNone(config.params)
        self.assertIsNotNone(config.params['apikey'])
        self.assertIsNotNone(config.mcurl)
        self.assertEqual(config.params['apikey'],"12345678901234567890123456789012")
        self.assertEqual(config.mcurl,"http://mctest.localhost/api")

