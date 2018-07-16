import unittest
import pytest
from random import randint
from materials_commons.api import api


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestApiProjectRaw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.access_user = "test@test.mc"

    def test_project_owner_raw(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])

    def test_all_projects_raw(self):
        # make sure that there is at least one project
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])
        project_id = raw_data['id']
        project_list = api.projects(apikey=self.apikey)
        self.assertTrue(len(project_list) > 1)
        found_project = None
        for project in project_list:
            if project['name'] == project_name:
                found_project = project
        self.assertIsNotNone(found_project)
        self.assertEqual(project_id, found_project['id'])

    def test_get_project_by_id_raw(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])
        project_id = raw_data['id']

        project = api.get_project_by_id(project_id, apikey=self.apikey)
        self.assertIsNotNone(project)
        self.assertEqual(project_name, project['name'])
        self.assertEqual(self.user, project['owner'])

    def test_update_project_raw(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])
        project_id = raw_data['id']

        new_name = "Updated-" + project_name
        new_description = "Updated-" + description
        project = api.update_project(project_id, new_name, new_description, apikey=self.apikey)
        self.assertIsNotNone(project)
        self.assertEqual(new_name, project['name'])
        self.assertEqual(self.user, project['owner'])

    def test_delete_project_raw(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])
        project_id = raw_data['id']
        results = api.delete_project(project_id, apikey=self.apikey)
        self.assertEqual(project_id, results['project_id'])
        project_list = api.projects(apikey=self.apikey)
        self.assertTrue(len(project_list) > 1)
        found_project = None
        for project in project_list:
            if project['name'] == project_name:
                found_project = project
        self.assertIsNone(found_project)
        pass

    def test_user_access_to_project_raw(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(project_name, raw_data['name'])
        self.assertEqual(self.user, raw_data['owner'])
        project_id = raw_data['id']

        value = api.users_with_access_to_project(project_id, apikey=self.apikey)
        user_list_raw = value['val']
        self.assertEqual(1, len(user_list_raw))
        self.assertEqual(self.user, user_list_raw[0]['user_id'])

        value = api.add_user_access_to_project(project_id, self.access_user, apikey=self.apikey)
        added_user = value['val']
        self.assertEqual(self.access_user, added_user)
        value = api.users_with_access_to_project(project_id, apikey=self.apikey)
        user_list_raw = value['val']
        self.assertEqual(2, len(user_list_raw))

        value = api.remove_user_access_to_project(project_id, self.access_user, apikey=self.apikey)
        removed_user = value['val']
        self.assertEqual(self.access_user, removed_user)
        value = api.users_with_access_to_project(project_id, apikey=self.apikey)
        user_list_raw = value['val']
        self.assertEqual(1, len(user_list_raw))
