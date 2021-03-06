import unittest
import pytest
from random import randint
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number

@pytest.mark.skip(reason="no way of currently testing this")
class TestDirectoryCreateFromList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_name = fake_name("TestDirectoryProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.project_name, description)
        cls.project = project

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)

    def test_basic_dir_list(self):
        project = self.project
        directory_path_list = ['/a/b/c', '/a/b/e', '/a/f/g']
        directory_table = project.add_directory_list(directory_path_list)
        self.assertIsNotNone(directory_table)
        for path in directory_path_list:
            self.assertIsNotNone(directory_table[path])
            self.assertEqual(directory_table[path].name,project.name + path)