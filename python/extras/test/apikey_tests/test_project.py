import unittest
from random import randint
from materials_commons.api import create_project, get_all_projects


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


# Note - methods in Project - tests moved to other test files
#
# Move to Directory
# def get_directory_list(self, path):
# def create_or_get_all_directories_on_path(self, path):
# def add_directory_list(self, path_list, top=None):

# Move to File
# def add_file_using_directory(self, directory, file_name, local_path, verbose=False, limit=50):
# def add_file_by_local_path(self, local_path, verbose=False, limit=50):
# def get_by_local_path(self, local_path):
# def file_exists_by_local_path(self, local_path, checksum=False):
# def add_directory_tree_by_local_path(self, local_path, verbose=False, limit=50):

# Move to Process
# def get_all_processes(self):
# def get_process_by_id(self, process_id):

# Moved to Sample
# def get_all_samples(self):
# def fetch_sample_by_id(self, sample_id):
# def get_sample_by_id(self, sample_id):

class TestProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.access_user = "test@test.mc"
        cls.another_apikey = "totally-bogus"
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)

    def test_project_base(self):
        self.assertTrue(hasattr(self.project, '_apikey'))
        self.assertIsNotNone(self.project._apikey)
        self.assertEqual(self.apikey, self.project._apikey)
        self.assertEqual(self.user, self.project.owner)

    def test_delete(self):
        # at lease one additional project
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        project = create_project(project_name, description, apikey=self.apikey)

        # Note: project list will include all projects to which the user has access; some may not be owned
        project_list = get_all_projects(apikey=self.apikey)
        found = None
        for probe in project_list:
            if probe.owner == self.user:
                self.assertTrue(hasattr(probe, '_apikey'))
                self.assertIsNotNone(probe._apikey)
                self.assertEqual(self.apikey, probe._apikey)
                if probe.id == project.id:
                    found = probe
        self.assertIsNotNone(found)
        found.delete()
        project_list = get_all_projects(apikey=self.apikey)
        found = None
        for probe in project_list:
            if probe.owner == self.user:
                self.assertTrue(hasattr(probe, '_apikey'))
                self.assertIsNotNone(probe._apikey)
                self.assertEqual(self.apikey, probe._apikey)
                if probe.id == project.id:
                    found = probe
        self.assertIsNone(found)

    def test_delete_multiple(self):
        # at lease one additional project
        project_name = fake_name("Test1ApikeyProject-")
        description = "Test project generated by automated test"
        project = create_project(project_name, description, apikey=self.apikey)

        # add project from another user to which test user has access
        project_name = fake_name("Test2ApikeyProject-")
        description = "Test project generated by automated test"
        another_project = create_project(project_name, description, apikey=self.another_apikey)
        another_project.add_user_to_access_list(self.user)

        # Note: project list will include all projects to which the user has access; some may not be owned
        project_list = get_all_projects(apikey=self.apikey)
        found = None
        for probe in project_list:
            if probe.owner == self.user:
                self.assertTrue(hasattr(probe, '_apikey'))
                self.assertIsNotNone(probe._apikey)
                self.assertEqual(self.apikey, probe._apikey)
                if probe.id == project.id:
                    found = probe
        self.assertIsNotNone(found)
        found.delete()
        project_list = get_all_projects(apikey=self.apikey)
        found = None
        for probe in project_list:
            if probe.owner == self.user:
                self.assertTrue(hasattr(probe, '_apikey'))
                self.assertIsNotNone(probe._apikey)
                self.assertEqual(self.apikey, probe._apikey)
                if probe.id == project.id:
                    found = probe
        self.assertIsNone(found)

    def test_create_experiment(self):
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        experiment = self.project.create_experiment(experiment_name, description)
        self.assertEqual(self.user, experiment.owner)
        self.assertEqual(self.project.id, experiment.project.id)

    def test_get_all_experiments(self):
        # at least one experiment
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        experiment = self.project.create_experiment(experiment_name, description)
        experiment_list = self.project.get_all_experiments()
        found = None
        for probe in experiment_list:
            self.assertEqual(self.user, probe.owner)
            if probe.id == experiment.id:
                found = probe
        self.assertIsNotNone(found)

    def test_get_top_directory(self):
        top_directory = self.project.get_top_directory()
        self.assertEqual(self.project.name, top_directory.name)
        self.assertEqual(self.project.name, top_directory.path)

    def test_get_directory_by_id(self):
        top_directory = self.project.get_top_directory()
        also_top_directory = self.project.get_directory_by_id(top_directory.id)
        self.assertEqual(self.project.name, also_top_directory.name)
        self.assertEqual(self.project.name, also_top_directory.path)

    def test_get_all_directories(self):
        # Note: Test assumes the 3 default directories!
        top_directory = self.project.get_top_directory()
        directory_list = self.project.get_all_directories()
        self.assertEqual(4, len(directory_list))
        found = None
        for probe in directory_list:
            if top_directory.id == probe.id:
                found = probe
        self.assertIsNotNone(found)
        self.assertEqual(self.project.name, found.name)

    def test_get_access_list(self):
        access_list = self.project.get_access_list()
        found = None
        for probe in access_list:
            if self.user == probe:
                found = probe
        self.assertIsNotNone(found)

    def test_add_user_to_access_list(self):
        self.project.add_user_to_access_list(self.access_user)
        access_list = self.project.get_access_list()
        found = None
        for probe in access_list:
            if self.access_user == probe:
                found = probe
        self.assertIsNotNone(found)

    def test_remove_user_from_access_list(self):
        self.project.add_user_to_access_list(self.access_user)
        access_list = self.project.get_access_list()
        found = None
        for probe in access_list:
            if self.access_user == probe:
                found = probe
        self.assertIsNotNone(found)
        self.project.remove_user_from_access_list(self.access_user)
        access_list = self.project.get_access_list()
        found = None
        for probe in access_list:
            if self.access_user == probe:
                found = probe
        self.assertIsNone(found)

class TestExperimentProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        project_name = fake_name("TestExperimentProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)

    def test_project_experiment_multiple(self):
        experiment1_name = fake_name("TestExperiment1-")
        experiment2_name = fake_name("TestExperiment1-")
        description = "Test experiment generated by automated test"

        experiment1 = self.project.create_experiment(experiment1_name, description)
        self.assertEqual(self.user, experiment1.owner)
        self.assertEqual(self.project.id, experiment1.project.id)

        experiment2 = self.project.create_experiment(experiment2_name, description)
        self.assertEqual(self.user, experiment2.owner)
        self.assertEqual(self.project.id, experiment2.project.id)

        experiment_list = self.project.get_all_experiments()
        found = None
        for probe in experiment_list:
            self.assertEqual(self.user, probe.owner)
            if probe.id == experiment1.id:
                found = probe
        self.assertIsNotNone(found)

        experiment_list = self.project.get_all_experiments()
        found = None
        for probe in experiment_list:
            self.assertEqual(self.user, probe.owner)
            if probe.id == experiment2.id:
                found = probe
        self.assertIsNotNone(found)
