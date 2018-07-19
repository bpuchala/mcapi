import unittest
from random import randint
from materials_commons.api import create_project, get_project_by_id, get_all_projects
from materials_commons.api import get_all_templates, get_all_users


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number

# -- Note:
# for the following - look in test_experiment.py
# def create_experiment_metadata(experiment_id, metadata):
# def get_experiment_metadata_by_experiment_id(experiment_id):
# def get_experiment_metadata_by_id(metadata_id):


class TestTopLevel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"

    def test_create_project(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        project = create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(self.user, project.owner)

    def test_get_project_by_id(self):
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        project = create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(self.user, project.owner)
        again_project = get_project_by_id(project.id, apikey=self.apikey)

    def test_get_all_projects(self):
        # at least one project
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        one_project = create_project(project_name, description, apikey=self.apikey)
        self.assertEqual(self.user, one_project.owner)

        # Note: project list will include all projects to which the user has access; some may not be owned
        project_list = get_all_projects(apikey=self.apikey)
        found = None
        for probe in project_list:
            if probe.owner == self.user:
                self.assertTrue(hasattr(probe, '_apikey'))
                self.assertIsNotNone(probe._apikey)
                self.assertEqual(self.apikey, probe._apikey)
                if probe.id == one_project.id:
                    found = probe
        self.assertIsNotNone(found)

    def test_get_all_users(self):
        user_list = get_all_users(apikey=self.apikey)
        found = None
        for user in user_list:
            if user.id == self.user:
                found = user
        self.assertIsNotNone(found)

    def test_get_all_templates(self):
        template_list = get_all_templates(apikey=self.apikey)
        found = None
        for template in template_list:
            if template.id == "global_Create Samples":
                found = template
        self.assertIsNotNone(found)
