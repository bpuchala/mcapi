import unittest
import datetime
from random import randint
from mcapi import api
from mcapi import create_project
from mcapi import Template


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestCreateSampleDate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_name = fake_name("TestingDate-")
        description = "Test project generated by automated test"
        cls.project = create_project(cls.project_name, description)
        cls.project_id = cls.project.id
        cls.experiment_name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(cls.experiment_name, description)
        cls.experiment_id = cls.experiment.id
        cls.test_date_value = 1485977519347 #February 1, 2017

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertEqual(self.experiment_id, self.experiment.id)

    def test_set_date_from_raw_data(self):

        process = self.experiment.create_process_from_template(Template.create)
        process.rename("Testing01")

        name_list = ['manufacturing_date']
        dict = process.get_setup_properties_as_dictionary()

        prop_list = []
        for name in name_list:
            prop = dict[name]
            if (prop):
                prop_list.append(prop)
        prop = prop_list[0]

        value = self.test_date_value

        payload = {
            "template_id":"global_Create Samples",
            "properties":[
                {"attribute":"manufacturing_date",
                "choices":[],
                "description":"",
                "name":"Manufacturing Date",
                "otype":"date",
                "required":False,
                "unit":"",
                "units":[],
                "value":value,
                "id":prop.id,
                "setup_id":prop.setup_id,
                "setup_attribute":"instrument"}]
        }

        api_url = "projects/" + self.project_id + \
                  "/experiments/" + self.experiment_id + \
                  "/processes/" + process.id

        results = api.put(api.use_remote().make_url_v2(api_url), payload)

        self.assertEqual(results['otype'],'process')
        self.assertEqual(results['setup'][0]['properties'][2]['value'],value)

    def test_setting_manufacturing_fixed_date_setup(self):

        process = self.experiment.create_process_from_template(Template.create)
        process.rename("Testing02")
        value = self.test_date_value
        process.set_value_of_setup_property('manufacturing_date', value)
        process_updated = process.update_setup_properties(['manufacturing_date'])
        self.assertEqual(process_updated.setup[0].properties[2].value,value)

    def test_setting_manufacturing_computed_date_setup(self):

        emperical_correction = 70319347

        # Note this method produces a date value that is two days short
        # That is Feb 2, 2017 shows up in the UI as Jan 31, 2017
        # The emperical_correction value above, determined by the differance
        # between the computed value (below) and the observed value (at the UI),
        # of self.test_date_value (at top of this code), makes the correction
        # to the computed value so that it matches the expected value (!!!)
        dt = datetime.date(2017, 2, 1)
        value = int((dt - datetime.date(1970, 1, 1)).total_seconds() * 1000.0)

        value = value + emperical_correction

        self.assertEqual(value,self.test_date_value)

        process = self.experiment.create_process_from_template(Template.create)
        process.rename("Testing03")
        process.set_value_of_setup_property('manufacturing_date', value)
        process_updated = process.update_setup_properties(['manufacturing_date'])
        self.assertEqual(process_updated.setup[0].properties[2].value,value)
