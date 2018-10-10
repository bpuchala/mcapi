import unittest
from random import randint
from materials_commons.api import create_project
from materials_commons.api import get_all_templates


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestProcessPropertyChoice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        cls.base_project = create_project(cls.base_project_name, description)
        cls.base_project_id = cls.base_project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        cls.base_experiment = cls.base_project.create_experiment(name, description)
        cls.base_experiment_id = cls.base_experiment.id
        template_table = cls.make_template_table()
        template_id = cls.template_id_with(template_table, "APT")
        cls.process = cls.base_experiment.create_process_from_template(template_id)

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)
        self.assertIsNotNone(self.base_experiment)
        self.assertIsNotNone(self.base_experiment.id)
        self.assertEqual(self.base_experiment_id, self.base_experiment.id)
        self.assertIsNotNone(self.process)
        self.assertIsNotNone(self.process.id)
        self.assertIsNotNone(self.process.process_type)
        self.assertEqual(self.process.process_type, 'measurement')
        self.assertFalse(self.process.does_transform)
        self.assertEqual(len(self.process.setup), 1)
        self.assertEqual(len(self.process.setup[0].properties), 10)

    def test_known_choice_selection(self):
        print("")
        properties_table = self.process.get_setup_properties_as_dictionary()
        choice_attributes = ['mode','evaporation_control','imaging_gas']
        for a in choice_attributes:
            self.assertIn(a, properties_table)
        choice_name_lookup = {}
        for choice in properties_table['mode'].choices:
            choice_name_lookup[choice['value']] = choice['name']
        # set by name
        self.process.set_value_of_setup_property('mode', choice_name_lookup['laser'])
        prop = self.process.get_setup_properties_as_dictionary()['mode']
        self.assertEqual(prop.attribute, "mode")
        self.assertEqual(prop.name, "Mode")
        self.assertEqual(prop.value['name'], 'Laser')
        self.assertEqual(prop.value['value'], 'laser')
        # set by value - override and push to database
        self.process.set_value_of_setup_property('mode', 'voltage')
        prop = self.process.get_setup_properties_as_dictionary()['mode']
        print(prop.value)
        self.assertEqual(prop.attribute, "mode")
        self.assertEqual(prop.name, "Mode")
        self.assertEqual(prop.value['name'], 'Voltage')
        self.assertEqual(prop.value['value'], 'voltage')
        new_process = self.process.update_setup_properties(['mode'])
        self.assertEqual(self.process.id, new_process.id)
        prop = new_process.get_setup_properties_as_dictionary()['mode']
        self.assertEqual(prop.attribute, "mode")
        self.assertEqual(prop.name, "Mode")
        self.assertEqual(prop.value['name'], 'Voltage')
        self.assertEqual(prop.value['value'], 'voltage')

    def test_unknown_choice_selection_for_other(self):
        print("")
        properties_table = self.process.get_setup_properties_as_dictionary()
        choice_attributes = ['mode','evaporation_control','imaging_gas']
        for a in choice_attributes:
            self.assertIn(a, properties_table)
        choice_name_lookup = {}
        print(properties_table['evaporation_control'].choices)
        for choice in properties_table['evaporation_control'].choices:
            choice_name_lookup[choice['value']] = choice['name']
        self.assertIn('other', choice_name_lookup)
        self.process.set_value_of_setup_property('evaporation_control', 'constant_detector_rate')
        prop = self.process.get_setup_properties_as_dictionary()['evaporation_control']
        print(prop.name, prop.attribute, prop.value)
        # self.assertEqual(prop.attribute, "evaporation_control")
        # self.assertEqual(prop.name, "Evaporation Control")
        # print(prop.value)
        # self.assertEqual(prop.value['name'], 'Other')
        # self.assertEqual(prop.value['value'], 'anything')
        #new_process = self.process.update_setup_properties(['mode'])
        #self.assertEqual(self.process.id, new_process.id)
        #prop = new_process.get_setup_properties_as_dictionary()['mode']
        #self.assertEqual(prop.attribute, "mode")
        #self.assertEqual(prop.name, "Mode")
        #self.assertEqual(prop.value['name'], 'Voltage')
        #self.assertEqual(prop.value['value'], 'voltage')



    @classmethod
    def make_template_table(cls):
        template_list = get_all_templates()
        table = {}
        for template in template_list:
            table[template.id] = template
        return table

    @classmethod
    def template_id_with(cls, table, match):
        found_id = None
        match = "global_{}".format(match)
        for key in table:
            if match == key:
                found_id = key
        return found_id