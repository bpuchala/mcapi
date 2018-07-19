import unittest
import pytest
from random import randint
from materials_commons.api import create_project, Experiment


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


@pytest.mark.skip("TestDirectory - later")
class TestDirectory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)

# from Project Move to Directory
# def get_directory_list(self, path):
# def create_or_get_all_directories_on_path(self, path):
# def add_directory_list(self, path_list, top=None):
# def add_directory_tree_by_local_path(self, local_path, verbose=False, limit=50):
# - redundent to test with multiple directories
# def get_directory_by_id(self, directory_id):
# def get_all_directories(self):

