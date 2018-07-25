import unittest
from random import randint
from materials_commons.api import get_all_templates
from materials_commons.api import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestExperimentSampleBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_project_name = fake_name("TestProject-")
        print(cls.base_project_name)
        description = "Test project generated by automated test"
        project = create_project(cls.base_project_name, description)
        cls.base_project_id = project.id
        cls.base_project = project
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        experiment = project.create_experiment(name, description)
        cls.experiment_name = name
        cls.experiment_description = description
        cls.experiment = experiment
        cls.templates = _make_template_table()

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertIsNotNone(self.experiment.name)
        self.assertEqual(self.experiment_name, self.experiment.name)
        self.assertIsNotNone(self.experiment.description)
        self.assertEqual(self.experiment_description, self.experiment.description)

    def test_is_sample_in_experiment(self):
        create_sample_template = _template_id_with(self.templates, "Create Sample")
        create_sample_process = \
            self.experiment.create_process_from_template(create_sample_template)
        sample_name = 'Test Sample 1'
        created_sample = create_sample_process.create_samples([sample_name])[0]

        transform_template = _template_id_with(self.templates, "Heat Treatment")
        transform_process = \
            self.experiment.create_process_from_template(transform_template)
        self.assertEqual(self.experiment.id, transform_process.experiment.id)

        transform_process.add_input_samples_to_process([created_sample])
        all_samples = self.experiment.get_all_samples()
        self.assertIsNotNone(all_samples)
        self.assertEqual(1, len(all_samples))

        first_sample = all_samples[0]
        self.assertEqual(sample_name, first_sample.name)

        transform_process.add_input_samples_to_process([created_sample])
        transform_process.decorate_with_output_samples()
        self.assertIsNotNone(transform_process.output_samples)
        self.assertTrue(len(transform_process.output_samples) > 0)
        transformed_sample = transform_process.output_samples[0]
        sample_id = transformed_sample.id

        samples = self.experiment.get_all_samples()
        found = None
        for sample in samples:
            if sample_id == sample.id:
                found = sample
        self.assertIsNotNone(found)
        self.assertEqual(found.name, created_sample.name)

        sample_by_id = self.experiment.get_sample_by_id(sample_id)
        self.assertEqual(sample_by_id.name, created_sample.name)

        sample_from_project1 = self.base_project.get_sample_by_id(sample_id)
        self.assertEqual(sample_from_project1.name, created_sample.name)

        sample_from_project2 = self.base_project.fetch_sample_by_id(sample_id)
        self.assertEqual(sample_from_project2.name, created_sample.name)

        sample_from_project3 = None
        samples = self.base_project.get_all_samples()
        for probe in samples:
            if sample_id == probe.id:
                sample_from_project3 = probe
        self.assertIsNotNone(sample_from_project3)
        self.assertEqual(sample_from_project3.name, created_sample.name)


class TestExperimentSampleNoTransform(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.base_project_name, description)
        cls.base_project_id = project.id
        cls.base_project = project
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        experiment = project.create_experiment(name, description)
        cls.experiment_name = name
        cls.experiment_description = description
        cls.experiment = experiment
        cls.templates = _make_template_table()

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertIsNotNone(self.experiment.name)
        self.assertEqual(self.experiment_name, self.experiment.name)
        self.assertIsNotNone(self.experiment.description)
        self.assertEqual(self.experiment_description, self.experiment.description)

    def test_add_sample_to_process_with_no_transform(self):
        # compare to lines 44-66 above
        create_sample_template = _template_id_with(self.templates, "Create Sample")
        create_sample_process = \
            self.experiment.create_process_from_template(create_sample_template)
        sample_name = 'Test Sample 2'
        created_sample = create_sample_process.create_samples([sample_name])[0]

        transform_template = _template_id_with(self.templates, "Heat Treatment")
        transform_process = \
            self.experiment.create_process_from_template(transform_template)
        self.assertEqual(self.experiment.id, transform_process.experiment.id)

        transform_process.add_input_samples_to_process([created_sample], transform=False)
        transform_process.decorate_with_output_samples()
        self.assertIsNotNone(transform_process.output_samples)
        self.assertTrue(len(transform_process.output_samples) == 0)


def _template_id_with(templates, match):
    found_id = None
    for key in templates:
        if match in key:
            found_id = key
    return found_id


def _make_template_table():
    ret = {}
    templates = get_all_templates()
    for t in templates:
        ret[t.id] = t
    return ret
