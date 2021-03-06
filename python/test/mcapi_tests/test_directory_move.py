import unittest
import pytest
from random import randint
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestDirectoryMove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_name = fake_name("TestMoveProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.project_name, description)
        cls.project_id = project.id
        cls.project = project

        cls.top_directory = project.get_top_directory()
        cls.test_dir_path_for_move = '/TestForMove'
        cls.directory_for_move = project.add_directory(cls.test_dir_path_for_move)
        cls.test_dir_path_a = "/TestForMove/A"
        cls.directory_a = project.add_directory(cls.test_dir_path_a)
        cls.test_dir_path_b = "/TestForMove/A/B"
        cls.directory_b = project.add_directory(cls.test_dir_path_b)
        cls.test_dir_path_c = "/TestForMove/A/B/C"
        cls.directory_c = project.add_directory(cls.test_dir_path_c)
        cls.test_dir_path_d = "/TestForMove/A/B/D"
        cls.directory_d = project.add_directory(cls.test_dir_path_d)
        cls.test_dir_path_e = "/TestForMove/A/E"
        cls.directory_e = project.add_directory(cls.test_dir_path_e)
        cls.test_dir_path_f = "/TestForMove/F"
        cls.directory_f = project.add_directory(cls.test_dir_path_f)

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertEqual(self.top_directory.name, self.project.name)
        self.assertEqual(self.directory_a.name, self.project.name + self.test_dir_path_a)
        self.assertEqual(self.directory_b.name, self.project.name + self.test_dir_path_b)

        directory_list = self.project.get_all_directories()
        self.assertIsNotNone(directory_list)
        self.assertEqual(len(directory_list), 8)
        self.assertEqual(directory_list[0].name, self.project.name)
        self.assertEqual(directory_list[1].name, self.project.name + self.test_dir_path_for_move)
        self.assertEqual(directory_list[2].name, self.project.name + self.test_dir_path_a)
        self.assertEqual(directory_list[3].name, self.project.name + self.test_dir_path_b)
        self.assertEqual(directory_list[4].name, self.project.name + self.test_dir_path_c)
        self.assertEqual(directory_list[5].name, self.project.name + self.test_dir_path_d)
        self.assertEqual(directory_list[6].name, self.project.name + self.test_dir_path_e)
        self.assertEqual(directory_list[7].name, self.project.name + self.test_dir_path_f)

    def test_move_directory(self):
        directory = self.directory_b
        target = self.directory_e
        self.assertEqual(directory._project, self.project)
        self.assertEqual(directory._parent_id,self.directory_a.id)
        self.assertEqual(directory.name, self.project.name + self.test_dir_path_b)
        self.assertEqual(target.name, self.project.name + self.test_dir_path_e)
        updatedDirectory = directory.move(target)
        self.assertEqual(updatedDirectory.path, self.project.name + "/TestForMove/A/E/B")
        self.assertEqual(updatedDirectory._project, self.project)
        self.assertEqual(updatedDirectory._parent_id,self.directory_e.id)
        self.assertEqual(updatedDirectory.id,directory.id)

        directory_list = self.project.get_all_directories()
        self.assertIsNotNone(directory_list)
        self.assertEqual(len(directory_list), 8)
        self.assertEqual(directory_list[0].name, self.project.name)
        self.assertEqual(directory_list[1].name, self.project.name + self.test_dir_path_for_move)
        self.assertEqual(directory_list[2].name, self.project.name + self.test_dir_path_a)
        self.assertEqual(directory_list[3].name, self.project.name + "/TestForMove/A/E")
        self.assertEqual(directory_list[4].name, self.project.name + "/TestForMove/A/E/B")
        self.assertEqual(directory_list[5].name, self.project.name + "/TestForMove/A/E/B/C")
        self.assertEqual(directory_list[6].name, self.project.name + "/TestForMove/A/E/B/D")
        self.assertEqual(directory_list[7].name, self.project.name + self.test_dir_path_f)

    def test_cannot_move_top_level_directory(self):
        top_directory = self.project.get_top_directory()
        self.assertEqual(top_directory.path, self.project.name)
        with pytest.raises(Exception):
            updatedDirectory = top_directory.move("XX")
        top_directory = self.project.get_top_directory()
        self.assertEqual(top_directory.path, self.project.name)
