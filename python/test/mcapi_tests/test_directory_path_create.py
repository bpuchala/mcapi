import unittest
from random import randint
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestDirectoryPathCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_project_name = fake_name("TestDirectoryProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.base_project_name, description)
        cls.base_project_id = project.id
        cls.base_project = project
        cls.test_dir_path = "/TestDir1/TestDir2/TestDir3"

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)

    def test_get_top_dir_by_path(self):
        directory1 = self.base_project.create_or_get_all_directories_on_path("/")[0]
        directory2 = self.base_project.get_top_directory()
        self.assertEqual(directory1.id, directory2.id)
        self.assertEqual(directory1._project, self.base_project)
        self.assertEqual(directory2._project, self.base_project)

    def test_create_dir_path_project(self):
        directory_list = self.base_project.create_or_get_all_directories_on_path(self.test_dir_path)
        self.assertIsNotNone(directory_list)
        last_directory = directory_list[-1]
        path1 = "/" + last_directory.name.split("/", 1)[1]
        path2 = self.test_dir_path
        if path2.endswith("/"):
            path2 = path2[:-1]
        self.assertEqual(path1, path2)
