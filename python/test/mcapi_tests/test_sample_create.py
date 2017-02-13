import unittest
from random import randint
from mcapi import set_remote_config_url
from mcapi import create_project, Template


url = 'http://mctest.localhost/api'


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestSampleCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_remote_config_url(url)
        cls.project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(cls.project_name, description)
        cls.project_id = cls.project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(name, description)
        cls.experiment_id = cls.experiment.id
        cls.process = cls.experiment.create_process_from_template(Template.create)
        cls.process_id = cls.process.id

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertEqual(self.experiment_id, self.experiment.id)
        self.assertIsNotNone(self.process)
        self.assertIsNotNone(self.process_id)
        self.assertIsNotNone(self.process.process_type)
        self.assertEqual(self.process.process_type, 'create')
        self.assertTrue(self.process.does_transform)

    def test_create_sample(self):
        sample_names = ['Test Sample 1', 'Test Sample 2']
        samples = self.process.create_samples(sample_names)
        self.assertIsNotNone(samples)
        sample = samples[0]
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.name)
        self.assertIsNotNone(sample.property_set_id)
        self.assertEqual(sample.name, sample_names[0])
        self.assertEqual(sample.project.id, self.project_id)
        self.assertEqual(sample.process.id, self.process_id)
        self.assertEqual(sample.process.experiment.id, self.experiment_id)
        self.assertTrue(len(self.experiment.samples) == 0, "The original experiment has no samples")
        updated_experiment = self.experiment.fetch_and_add_samples(self.process)
        self.assertTrue(len(updated_experiment.samples) == 2, "The experiment now has 2 samples")
        experiment_samples = updated_experiment.samples
        found_sample = None
        for es in experiment_samples:
            if es.id == sample.id:
                found_sample = es
        self.assertIsNotNone(found_sample,"The original sample is in the experiment")
        self.assertEqual(found_sample.project.id, self.project_id)
        self.assertEqual(found_sample.experiment.id, self.experiment_id)


