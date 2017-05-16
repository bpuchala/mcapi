import unittest
from random import randint
from mcapi import create_project, Template


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestSampleAssociate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_project_name = "Project-TestSampleAssociate"
        description = "Test project generated by automated test"
        cls.base_project = create_project(cls.base_project_name, description)
        cls.base_project_id = cls.base_project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        cls.base_experiment = cls.base_project.create_experiment(name, description)
        cls.base_experiment_id = cls.base_experiment.id
        cls.base_create_sample_process = \
            cls.base_experiment.create_process_from_template(Template.create)
        cls.base_sample = cls.base_create_sample_process.create_samples(['Test Sample 1'])[0]
        cls.base_compute_process = \
            cls.base_experiment.create_process_from_template(Template.compute)

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)

        self.assertIsNotNone(self.base_experiment)
        self.assertIsNotNone(self.base_experiment.id)
        self.assertEqual(self.base_experiment_id, self.base_experiment.id)

        self.assertIsNotNone(self.base_create_sample_process)
        self.assertIsNotNone(self.base_create_sample_process.id)
        self.assertIsNotNone(self.base_create_sample_process.process_type)
        self.assertEqual(self.base_create_sample_process.process_type, 'create')
        self.assertTrue(self.base_create_sample_process.does_transform)

        self.assertIsNotNone(self.base_sample.id)
        self.assertIsNotNone(self.base_sample.name)

        self.assertIsNotNone(self.base_compute_process)
        self.assertIsNotNone(self.base_compute_process.id)
        self.assertIsNotNone(self.base_compute_process.process_type)
        self.assertEqual(self.base_compute_process.process_type, 'analysis')
        self.assertFalse(self.base_compute_process.does_transform)

    def test_associate_sample_with_process(self):
        process_with_sample = \
            self.base_compute_process.add_input_samples_to_process([self.base_sample])
        # process_with_sample = process_with_sample.fill_in_input_samples()
        self.assertEqual(process_with_sample.name, 'Computation')
        self.assertEqual(len(process_with_sample.input_samples), 1)
        self.assertEqual(process_with_sample.input_samples[0].name, self.base_sample.name)
        for sample in process_with_sample.input_samples:
            sample.decorate_with_processes()
        found_process = None
        print ''
        print '----'
        print process_with_sample.input_samples
        print process_with_sample.input_samples[0]
        print process_with_sample.input_samples[0].processes
        print '----'
        for process in process_with_sample.input_samples[0].processes:
            print process.process_type
            if process.process_type == 'analysis':
                found_process = process
        print '----'
        self.assertIsNotNone(found_process)
        self.assertEqual(found_process.id, process_with_sample.id)
