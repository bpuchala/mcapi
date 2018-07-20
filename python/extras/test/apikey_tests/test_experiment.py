import unittest
import pytest
from random import randint
from materials_commons.api import create_project, Template

def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


# Note: Experiment methods - testing moved to Sample
# def get_sample_by_id(self, sample_id):
# def get_all_samples(self):
# def decorate_with_samples(self):

class TestExperiment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.another_user = "test@test.mc"
        cls.another_apikey = "totally-bogus"
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(experiment_name, description)

    def test_experiment_rename(self):
        experiment_name = fake_name("TestApikeyExperiment-")
        update = self.experiment.rename(experiment_name)
        self.assertEqual(self.experiment.id, update.id)
        self.assertEqual(experiment_name, update.name)

    def test_experiment_delete(self):
        # another experiment
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        experiment = self.project.create_experiment(experiment_name, description)

        experiment_list = self.project.get_all_experiments()
        found = None
        for probe in experiment_list:
            if experiment.id == probe.id:
                found = experiment
        self.assertIsNotNone(found)
        experiment.delete()
        experiment_list = self.project.get_all_experiments()
        found = None
        for probe in experiment_list:
            if experiment.id == probe.id:
                found = experiment
        self.assertIsNone(found)

    def test_experiment_create_process_from_template(self):
        template_id = Template.create
        process = self.experiment.create_process_from_template(template_id)
        self.assertEqual(self.user, process.owner)

    def test_experiment_get_process_by_id(self):
        template_id = Template.create
        process = self.experiment.create_process_from_template(template_id)
        self.assertEqual(self.user, process.owner)
        probe = self.experiment.get_process_by_id(process.id)
        self.assertEqual(self.user, probe.owner)
        self.assertEqual(process.name, probe.name)

    def test_experiment_get_all_processes(self):
        template_id = Template.create
        process = self.experiment.create_process_from_template(template_id)
        self.assertEqual(self.user, process.owner)
        process_list = self.experiment.get_all_processes()
        found = None
        for probe in process_list:
            if probe.id == process.id:
                found = probe
        self.assertIsNotNone(found)


class TestExperimentDecorateWithSamples(unittest.TestCase):
    # need a isolated experiment for this test
    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.another_user = "test@test.mc"
        cls.another_apikey = "totally-bogus"
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(experiment_name, description)

    def test_experiment_decorate_with_processes(self):
        template_id = Template.create
        process = self.experiment.create_process_from_template(template_id)
        process_list = self.experiment.processes
        self.assertEqual(0, len(process_list))
        self.experiment.decorate_with_processes()
        process_list = self.experiment.processes
        self.assertEqual(1, len(process_list))
        self.assertEqual(process.id, process_list[0].id)

