import unittest
from random import randint
from mcapi import api
from mcapi import Remote
from mcapi import Config
from mcapi import create_project, create_experiment, create_process_from_template, create_samples

url = 'http://mctest.localhost/api'

def fake_name(prefix):
    number="%05d" % randint(0,99999)
    return prefix+number

class TestProcess(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        config = Config()
        api.set_remote(Remote(config=Config(config={'mcurl': url})))
        self.base_project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        self.base_project = create_project(self.base_project_name, description)
        self.base_project_id = self.base_project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        self.base_experiment = create_experiment(self.base_project_id,name, description)
        self.base_experiment_id = self.base_experiment.id
        template_id = "global_Create Samples"
        self.base_process = create_process_from_template(self.base_project_id,self.base_experiment_id,template_id)
        self.base_process_id = self.base_process.id

    def test_is_setup_correctly(self):
        self.assertEqual(api.use_remote().mcurl,url)
        self.assertIsNotNone(api.use_remote().config.params['apikey'])
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)
        self.assertIsNotNone(self.base_experiment)
        self.assertIsNotNone(self.base_experiment.id)
        self.assertEqual(self.base_experiment_id, self.base_experiment.id)
        self.assertIsNotNone(self.base_process)
        self.assertIsNotNone(self.base_process_id)
        self.assertIsNotNone(self.base_process.process_type)
        self.assertEqual(self.base_process.process_type, 'create')
        self.assertTrue(self.base_process.does_transform)

    def test_create_sample(self):
        sample_names = ['Test Sample 1']
        samples = create_samples(self.base_project_id, self.base_process_id, sample_names)
        self.assertIsNotNone(samples)
        sample = samples[0]
        print "sample: ",sample.id, sample.name, sample.property_set_id
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.name)
        self.assertIsNotNone(sample.property_set_id)
        self.assertEqual(sample.name,sample_names[0])
        self.assertTrue(False)


