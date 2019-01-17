import unittest
import pytest
from random import randint
from materials_commons.api import api
from .apikey_helper_utils import _upload_generic_test_file
from .apikey_helper_utils import FileTestException


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestApiFileBasicRaw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(cls.project_name, description, apikey=cls.apikey)
        cls.project_id = raw_data['id']
        try:
            file_record_raw = _upload_generic_test_file(cls.project_id, cls.apikey)
            cls.file_id = file_record_raw['id']
            cls.file_name = file_record_raw['name']
        except FileTestException:
            pytest.fail("Unexpected, exception", pytrace=True)

    def test_file_rename_raw(self):
        new_file_name = "RENAME-" + self.file_name
        file_record_raw = api.file_rename(
            self.project_id, self.file_id, new_file_name, apikey=self.apikey)
        self.assertEqual('datafile', file_record_raw['otype'])
        self.assertEqual(new_file_name, file_record_raw['name'])
        self.assertEqual(self.user, file_record_raw['owner'])

    def test_file_move_raw(self):
        results = api.directory_by_id(self.project_id, 'top', apikey=self.apikey)
        self.assertEqual(results['name'], self.project_name)
        directory_id = results['id']
        sub_directory_name = "/test"
        sub_directory_list = [
            sub_directory_name
        ]
        results = api.directory_create_subdirectories_from_path_list(
            self.project_id, directory_id, sub_directory_list, apikey=self.apikey)
        all_dirs_dict = results['val']
        self.assertEqual(1, len(all_dirs_dict))
        key = self.project_name + sub_directory_name
        sub_directory_record_raw = all_dirs_dict[key]
        new_directory_id = sub_directory_record_raw['id']
        file_record_raw = api.file_move(
            self.project_id, directory_id, new_directory_id, self.file_id, apikey=self.apikey)
        self.assertEqual('datafile', file_record_raw['otype'])
        self.assertEqual(self.file_name, file_record_raw['name'])
        self.assertEqual(self.user, file_record_raw['owner'])
        self.assertEqual(self.file_id, file_record_raw['id'])
        directory_record_raw = api.directory_by_id(self.project_id, new_directory_id, apikey=self.apikey)
        children = directory_record_raw['children']
        self.assertEqual(1, len(children))
        dir_file_raw = children[0]
        self.assertEqual('file', dir_file_raw['otype'])
        self.assertEqual(self.file_name, dir_file_raw['name'])
        self.assertEqual(self.file_id, dir_file_raw['id'])
        self.assertEqual(key + "/" + self.file_name, dir_file_raw['path'])