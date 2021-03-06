import unittest
import pytest
from os import environ
from os import path as os_path
from mcapi import use_remote, set_remote
import demo_project as demo


class TestDemoProject(unittest.TestCase):
    def test_build_demo_project(self):
        remote = use_remote()
        save_mcurl = remote.config.mcurl
        with pytest.raises(Exception) as exception_info:
            host = "http://noda.host"
            remote.config.mcurl = host + "/api"
            set_remote(remote)

            builder = demo.DemoProject(self._make_test_dir_path())

            builder.build_project()

        remote.config.mcurl = save_mcurl
        set_remote(remote)
        self.assertTrue(str(exception_info.type).find("ConnectionError") > 0)
        self.assertTrue(str(exception_info.value).find("host='noda.host'") > 0)

    def _make_test_dir_path(self):
        self.assertTrue('TEST_DATA_DIR' in environ)
        test_path = os_path.abspath(environ['TEST_DATA_DIR'])
        self.assertIsNotNone(test_path)
        self.assertTrue(os_path.isdir(test_path))
        test_path = os_path.join(test_path, 'demo_project_data')
        self.assertIsNotNone(test_path)
        self.assertTrue(os_path.isdir(test_path))
        return test_path
