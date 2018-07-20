import unittest
import pytest
from random import randint
from materials_commons.api import api
from .apikey_helper_utils import _upload_generic_test_file
from .apikey_helper_utils import FileTestException
from materials_commons.api import Template


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestApiFileProcessSampleRaw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        raw_data = api.create_project(cls.project_name, description, apikey=cls.apikey)
        cls.project_id = raw_data['id']
        experiment_name = fake_name("TestExperiment-")
        experiment_description = "Test experiment generated by automated test"
        experiment_raw = api.create_experiment(
            cls.project_id, experiment_name, experiment_description, apikey=cls.apikey)
        cls.experiment_id = experiment_raw['id']
        cls.template_id = Template.create
        process_record_raw = api.create_process_from_template(
            cls.project_id, cls.experiment_id, cls.template_id, apikey=cls.apikey)
        cls.process_id = process_record_raw['id']
        cls.sample_name = "TestSample1"
        results = api.create_samples_in_project(
            cls.project_id, cls.process_id, [cls.sample_name], apikey=cls.apikey)
        sample_list_raw = results['samples']
        sample_raw = sample_list_raw[0]
        cls.sample_id = sample_raw['id']
        api.add_samples_to_experiment(
            cls.project_id, cls.experiment_id, [sample_raw['id']], apikey=cls.apikey)

        try:
            file_record_raw = _upload_generic_test_file(cls.project_id, cls.apikey)
            cls.file_id = file_record_raw['id']
            cls.file_name = file_record_raw['name']
        except FileTestException:
            pytest.fail("Unexpected, exception", pytrace=True)

    def test_add_files_to_process_raw(self):
        process_record_raw = api.add_files_to_process(
            self.project_id, self.experiment_id, self.process_id, self.template_id,
            [self.file_id], apikey=self.apikey)
        self.assertEqual("process", process_record_raw['otype'])
        self.assertEqual(self.user, process_record_raw['owner'])
        process_file_list_raw = api.get_all_files_for_process(
            self.project_id, self.experiment_id, self.process_id, apikey=self.apikey)
        self.assertEqual(1, len(process_file_list_raw))
        process_file_raw = process_file_list_raw[0]
        self.assertEqual('datafile', process_file_raw['otype'])
        self.assertEqual(self.file_name, process_file_raw['name'])
        self.assertEqual(self.user, process_file_raw['owner'])
        self.assertEqual(self.process_id, process_file_raw['process_id'])
        self.assertEqual(self.file_id, process_file_raw['id'])

    def test_link_files_to_sample_raw(self):
        flag = api.link_files_to_sample(
            self.project_id, self.sample_id, [self.file_id], apikey=self.apikey)
        self.assertTrue(flag)
        sample_record_raw = api.get_project_sample_by_id(self.project_id, self.sample_id, apikey=self.apikey)
        self.assertEqual(1, len(sample_record_raw['files']))
        sample_file_raw = sample_record_raw['files'][0]
        self.assertEqual('datafile', sample_file_raw['otype'])
        self.assertEqual(self.file_name, sample_file_raw['name'])
        self.assertEqual(self.user, sample_file_raw['owner'])
        self.assertEqual(self.sample_id, sample_file_raw['sample_id'])
        self.assertEqual(self.file_id, sample_file_raw['id'])
