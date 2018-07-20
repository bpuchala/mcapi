import unittest
import pytest
from random import randint
from materials_commons.api import create_project, get_all_templates, Template
from .apikey_helper_utils import find_template_id_from_match, make_template_table


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


# Process methods moved to test for File
# def get_all_files(self):
# def add_files(self, files_list):

# Process methods moved to separate test: TestProcessSampleMeasurement
# def make_list_of_samples_for_measurement(self, samples):
# def create_measurement(self, data):
# def set_measurements_for_process_samples(self, measurement_property, measurements):
# def set_measurement(self, attribute, measurement_data, name=None):
# def add_integer_measurement(self, attrname, value, name=None):
# def add_number_measurement(self, attrname, value, name=None):
# def add_boolean_measurement(self, attrname, value, name=None):
# def add_string_measurement(self, attrname, value, name=None):
# def add_file_measurement(self, attrname, file, name=None):
# def add_sample_measurement(self, attrname, sample, name=None):
# def add_list_measurement(self, attrname, value, value_type, name=None):
# def add_numpy_matrix_measurement(self, attrname, value, name=None):
# def add_selection_measurement(self, attrname, value, name=None):
# def add_vector_measurement(self, attrname, value, name=None):

class TestProcess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.another_user = "test@test.mc"
        cls.another_apikey = "totally-bogus"
        cls.templates = make_template_table(get_all_templates())
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(experiment_name, description)
        cls.process = cls.experiment.create_process_from_template(Template.create)

    @pytest.mark.skip("TestProcess rename")
    def test_process_rename(self):
        process = self.experiment.create_process_from_template(Template.create)
        new_name = 'new_name'
        update = process.rename(new_name)
        self.assertEqual(new_name, update.name)
        self.assertEqual(self.user, update.owner)

    @pytest.mark.skip("TestProcess delete")
    def test_process_delete(self):
        process = self.experiment.create_process_from_template(Template.create)
        self.assertEqual(self.user, process.owner)
        process_list = self.experiment.get_all_processes()
        found = None
        for probe in process_list:
            if probe.id == process.id:
                found = probe
        self.assertIsNotNone(found)
        process.delete()
        self.assertEqual(self.user, process.owner)
        process_list = self.experiment.get_all_processes()
        found = None
        for probe in process_list:
            if probe.id == process.id:
                found = probe
        self.assertIsNone(found)

    @pytest.mark.skip("TestProcess set notes")
    def test_process_set_notes(self):
        process_notes_value = "An experimental process with notes"
        process_notes_value_expected = "<p>" + process_notes_value + "</p>"
        process = self.process.set_notes(process_notes_value)
        self.assertEqual(process.description, process_notes_value_expected)
        self.assertEqual(process.notes, process_notes_value_expected)

    @pytest.mark.skip("TestProcess add notes")
    def test_process_add_to_notes(self):
        process_notes_value = "An experimental process with notes"
        process_notes_value_expected = "<p>" + process_notes_value + "</p>"
        process = self.process.set_notes(process_notes_value)
        self.assertEqual(process.description, process_notes_value_expected)
        self.assertEqual(process.notes, process_notes_value_expected)
        process = process.add_to_notes(process_notes_value)
        process_notes_value_expected = process_notes_value_expected + "\n" + process_notes_value_expected
        self.assertEqual(process.notes, process_notes_value_expected)

    @pytest.mark.skip("TestProcess create samples")
    def test_process_create_samples(self):
        create_process = self.experiment.create_process_from_template(Template.create)
        sample_name = fake_name("TestSample-")
        sample_names = [sample_name]
        samples = create_process.create_samples(sample_names)
        self.assertEqual(1, len(samples))
        sample = samples[0]
        self.assertEqual(sample_name, sample.name)
        self.assertEqual(self.user, sample.owner)

    @pytest.mark.skip("TestProcess get all samples")
    def test_process_get_all_samples(self):
        create_process = self.experiment.create_process_from_template(Template.create)
        sample_name = fake_name("TestSample-")
        sample_names = [sample_name]
        samples = create_process.create_samples(sample_names)
        self.assertEqual(1, len(samples))
        sample = samples[0]
        samples = create_process.get_all_samples()
        found = None
        for probe in samples:
            if probe.id == sample.id:
                found = probe
        self.assertIsNotNone(found)
        self.assertEqual(sample_name, found.name)

    @pytest.mark.skip("TestProcess link samples")
    def test_process_link_process_with_samples(self):
        create_process = self.experiment.create_process_from_template(Template.create)
        sample_name = fake_name("TestSample-")
        sample_names = [sample_name]
        samples = create_process.create_samples(sample_names)
        self.assertEqual(1, len(samples))
        sample = samples[0]

        ht_template = find_template_id_from_match(self.templates, "Heat Treatment")
        self.assertIsNotNone(ht_template)
        ht_process = self.experiment.create_process_from_template(ht_template)
        self.assertEqual(ht_template, ht_process.template_id)

        ht_process.add_input_samples_to_process([sample])
        self.assertEqual(1, len(ht_process.input_samples))
        self.assertEqual(0, len(ht_process.output_samples))
        ht_process = ht_process.decorate_with_input_samples()
        ht_process = ht_process.decorate_with_output_samples()
        self.assertEqual(1, len(ht_process.input_samples))
        self.assertEqual(0, len(ht_process.output_samples))
        # unexpected results, above!!!


class TestProcessProperties(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = "another@test.mc"
        cls.apikey = "another-bogus-account"
        cls.another_user = "test@test.mc"
        cls.another_apikey = "totally-bogus"
        cls.templates = make_template_table(get_all_templates())
        project_name = fake_name("TestApikeyProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(project_name, description, apikey=cls.apikey)
        experiment_name = fake_name("TestApikeyExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(experiment_name, description)
        cls.create_process = cls.experiment.create_process_from_template(Template.create)
        ht_template = find_template_id_from_match(cls.templates, "Heat Treatment")
        cls.ht_process = cls.experiment.create_process_from_template(ht_template)

    @pytest.mark.skip("TestProcessProperties")
    def test_get_setup_properties_as_dictionary(self):
        # for create process
        table = self.create_process.get_setup_properties_as_dictionary()
        self.assertTrue('manufacturer' in table)
        self.assertTrue('supplier' in table)

    @pytest.mark.skip("TestProcessProperties")
    def test_is_known_setup_property(self):
        # for create process
        self.assertTrue(self.create_process.is_known_setup_property('supplier'))

    @pytest.mark.skip("TestProcessProperties")
    def test_set_known_setup_property(self):
        # for Heat Treatment Process
        process = self.ht_process
        process.set_value_of_setup_property('temperature', 100)
        process.set_unit_of_setup_property('temperature', 'C')
        process = process.update_setup_properties(['temperature'])
        table = process.get_setup_properties_as_dictionary()
        self.assertTrue('temperature' in table)
        setup_property = table['temperature']
        self.assertEqual(100, setup_property.value)
        self.assertEqual('C', setup_property.unit)

        process = self.experiment.get_process_by_id(process.id)
        process = process.update_setup_properties(['temperature'])
        table = process.get_setup_properties_as_dictionary()
        self.assertTrue('temperature' in table)
        setup_property = table['temperature']
        self.assertEqual(100, setup_property.value)
        self.assertEqual('C', setup_property.unit)

    @pytest.mark.skip("TestProcessProperties")
    def test_update_additional_setup_properties(self):
        # for Heat Treatment Process
        process = self.ht_process
        entry_list = [
            {
                "name": "lighting",
                "attribute": "lighting",
                "value": "blue",
                "unit": None,
                "otype": "string"
            },
            {
                "name": "speed",
                "attribute": "speed",
                "value": "1000",
                "unit": "m/s",
                "otype": "number"
            },
        ]
        process = process.update_additional_setup_properties(entry_list)
        # get "process" setup - Note, not fully developed in code!
        process_setup_raw = None
        for item in process.setup:
            if item.input_data['attribute'] == 'process':
                process_setup_raw = item.input_data['properties']
        self.assertIsNotNone(process_setup_raw)
        attribute_speed = None
        attribute_lighting = None
        for item in process_setup_raw:
            attribute = item['attribute']
            if attribute == "speed":
                attribute_speed = item
            if attribute == 'lighting':
                attribute_lighting = item
        self.assertIsNotNone(attribute_speed)
        self.assertIsNotNone(attribute_lighting)
        self.assertEqual("1000", attribute_speed['value'])
        self.assertEqual("m/s", attribute_speed['unit'])
        self.assertEqual("blue", attribute_lighting['value'])
        self.assertEqual('', attribute_lighting['unit'])


# from Project
# def get_all_processes(self):
# def get_process_by_id(self, process_id):

class TestProcessForProject(unittest.TestCase):
    @pytest.mark.skip("TestProcess TestProcessForProject")
    def any_test(self):
        pass
# from Project
# def get_all_processes(self):
# def get_process_by_id(self, process_id):

