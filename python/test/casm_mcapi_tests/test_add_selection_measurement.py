import unittest
from random import randint
from mcapi import set_remote_config_url
from mcapi import create_project, Template
from casm_mcapi import _add_selection_measurement

url = 'http://mctest.localhost/api'


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestAddChoiceMeasurements(unittest.TestCase):
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
        cls.process = cls.experiment.create_process_from_template(
            Template.primitive_crystal_structure)
        cls.sample_name = "pcs-sample-1"
        cls.sample = cls.process.create_samples(sample_names=[cls.sample_name])[0]

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
        self.assertIsNotNone(self.process.id)
        self.assertIsNotNone(self.process.process_type)
        self.assertEqual(self.process.process_type, 'create')
        self.assertTrue(self.process.does_transform)

        sample = self.sample
        samples = self.process.output_samples
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.name)
        self.assertIsNotNone(sample.property_set_id)
        self.assertEqual(sample.name, self.sample_name)
        self.assertEqual(sample.name, samples[0].name)

    def test_measurement_attribute_lattice_system_direct(self):
        choices = \
            [
                {"name": "Triclinic", "value": "triclinic"},  # 0
                {"name": "Monoclinic", "value": "monoclinic"},  # 1
                {"name": "Orthorhombic", "value": "orthorhombic"},  # 2
                {"name": "Tetragonal", "value": "tetragonal"},  # 3
                {"name": "Hexagonal", "value": "hexagonal"},  # 4
                {"name": "Rhombohedral", "value": "rhombohedral"},  # 5
                {"name": "Cubic", "value": "cubic"}  # 6
            ]
        value = choices[4]['value']
        name = "Lattice System"
        attribute = "lattice_system"

        data = {"name": name,
                "attribute": attribute,
                "otype": "selection",
                "unit": "",
                "units": [],
                "value": value,
                "is_best_measure": True}
        property_data = {
            "name": "Lattice System",
            "attribute": "lattice_system"
        }
        measurement = self.process.create_measurement(data=data)
        process_out = self.process.set_measurements_for_process_samples(
            property_data, [measurement])
        sample_out = process_out.output_samples[0]
        properties_out = sample_out.properties
        table = self.make_properties_dictionary(properties_out)
        property_data = table[name]
        self.assertEqual(len(property_data.best_measure), 1)
        measurement_out = property_data.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "selection")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value, value)

    def test_measurement_attribute_lattice_system(self):
        choices = \
            [
                {"name": "Triclinic", "value": "triclinic"},  # 0
                {"name": "Monoclinic", "value": "monoclinic"},  # 1
                {"name": "Orthorhombic", "value": "orthorhombic"},  # 2
                {"name": "Tetragonal", "value": "tetragonal"},  # 3
                {"name": "Hexagonal", "value": "hexagonal"},  # 4
                {"name": "Rhombohedral", "value": "rhombohedral"},  # 5
                {"name": "Cubic", "value": "cubic"}  # 6
            ]
        value = choices[4]['value']
        name = "Lattice System"
        attribute = "lattice_system"

        process = _add_selection_measurement(
            self.process, attribute, value, name=name)
        sample_out = process.output_samples[0]
        properties_out = sample_out.properties
        table = self.make_properties_dictionary(properties_out)
        selected_property = table[name]
        self.assertEqual(len(selected_property.best_measure), 1)
        measurement_out = selected_property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "selection")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value, value)

    def make_properties_dictionary(self, properties):
        ret = {}
        for the_property in properties:
            name = the_property.name
            ret[name] = the_property
        return ret
