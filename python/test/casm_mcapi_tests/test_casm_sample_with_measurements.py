import unittest
import numpy
from os import environ
from os import path as os_path
from random import randint
from mcapi import set_remote_config_url
from mcapi import create_project
from casm_mcapi import _add_string_measurement,\
    _add_numpy_matrix_measurement, _add_vector_measurement,\
    _add_list_measurement, _add_integer_measurement, _add_file_measurement


url = 'http://mctest.localhost/api'


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number

class TestPrinSample(unittest.TestCase):

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

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertEqual(self.experiment_id, self.experiment.id)

    def test_prim_sample(self):
        self.project.prim = self.mock_prim()
        sample_name = "Test Sample"
        directory = self.project.get_top_directory()
        file_name = 'fractal.jpg'
        file_path = self.make_test_dir_path(file_name)
        mcfile = self.project.add_file_using_directory(directory,file_name,file_path)

        process = self.create_prim_sample(self.experiment, self.project, sample_name, mcfile)
        self.assertIsNotNone(process)
        self.assertIsNotNone(process.id)
        self.assertIsNotNone(process.process_type)
        self.assertEqual(process.process_type, 'create')
        self.assertTrue(process.does_transform)
        sample_out = process.output_samples[0]
        self.assertIsNotNone(sample_out)
        self.assertEqual(sample_out.name,sample_name)
        properties_out = sample_out.properties
        table = self.make_properties_dictionary(properties_out)
        props = self.project.prim
        basic_tests = [
            {'type': 'string', 'name': 'name', 'value': self.project.name},
            {'type': 'string', 'name': 'lattice_point_group_schonflies', 'value': props.lattice_symmetry_s},
            {'type': 'string', 'name': 'lattice_point_group_hermann_mauguin', 'value': props.lattice_symmetry_hm},
            {'type': 'string', 'name': 'lattice_system', 'value': props.lattice_system},
            {'type': 'string', 'name': 'crystal_point_group_schonflies', 'value': props.crystal_symmetry_s},
            {'type': 'string', 'name': 'crystal_point_group_hermann_mauguin', 'value': props.crystal_symmetry_hm},
            {'type': 'string', 'name': 'crystal_family', 'value': props.crystal_family},
            {'type': 'string', 'name': 'crystal_system', 'value': props.crystal_system},
            {'type': 'string', 'name': 'space_group_number', 'value': props.space_group_number},
            {'type': 'string', 'name': 'degrees_of_freedom', 'value': props.degrees_of_freedom},
            {'type': 'integer', 'name': 'n_elements', 'value': len(props.elements)},
            {'type': 'integer', 'name': 'n_components', 'value': len(props.components)},
            {'type': 'integer', 'name': 'n_independent_compositions', 'value': props.n_independent_compositions}
        ]
        for t in basic_tests:
            self.assert_basic_property(table,t['type'],t['name'],t['value'])

        name = 'lattice_matrix'
        property = table[name]
        attribute = name
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, 'matrix')
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value['otype'],'float')
        self.assertEqual(measurement_out.value['otype'], 'float')
        self.assertEqual(measurement_out.value['dimensions'],list(props.lattice_matrix.shape))
        self.assertEqual(measurement_out.value['otype'],'float')

        resulting_value = numpy.array(measurement_out.value['value'])
        self.assertTrue(numpy.array_equal(resulting_value, props.lattice_matrix))
        self.assertEqual(resulting_value.shape,props.lattice_matrix.shape)

        name = 'lattice_parameters'
        property = table[name]
        attribute = name
        value = props.lattice_parameters
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "vector")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value['otype'], 'float')
        self.assertEqual(measurement_out.value['dimensions'], len(value))
        self.assertEqual(measurement_out.value['value'], value)


        name = 'casm_prism_file'
        property = table[name]
        attribute = name
        file = mcfile
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "file")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value['file_id'], file.id)
        self.assertEqual(measurement_out.value['file_name'], file.name)

        name = 'elements'
        property = table[name]
        attribute = name
        value = props.elements
        value_type = 'string'
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "vector")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value['otype'], value_type)
        self.assertEqual(measurement_out.value['dimensions'], len(value))
        self.assertEqual(measurement_out.value['value'], value)

        name = 'components'
        property = table[name]
        attribute = name
        value = props.elements
        value_type = 'string'
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "vector")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value['otype'], value_type)
        self.assertEqual(measurement_out.value['dimensions'], len(value))
        self.assertEqual(measurement_out.value['value'], value)


    def assert_basic_property(self,table,type,name,value):
        message = "Property: " + name
        property = table[name]
        attribute = name
        self.assertEqual(len(property.best_measure),1)
        measurement_out = property.best_measure[0]
        self.assertEqual(measurement_out.name, name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, type)
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value, value, message)

    def make_test_dir_path(self, file_name):
        self.assertTrue('TEST_DATA_DIR' in environ)
        test_path = os_path.abspath(environ['TEST_DATA_DIR'])
        self.assertIsNotNone(test_path)
        self.assertTrue(os_path.isdir(test_path))
        test_file = os_path.join(test_path, 'test_upload_data', file_name)
        self.assertTrue(os_path.isfile(test_file))
        return test_file

    def make_properties_dictionary(self,properties):
        ret = {}
        for property in properties:
            name = property.name
            ret[name] = property
        return ret

    def create_prim_sample(self, expt, casm_proj, sample_name, mcfile):
        """
        Create a CASM Primitive Crystal Structure Sample

        Assumes expt.project.path exists and adds files relative to that path.

        Arguments:

            expt: mcapi.Experiment object

            casm_proj: casm.project.Project object

            sample_name: str
              Name for sample, default is: casm_proj.name + ".prim"

        Returns:

            create_sample_process: mcapi.Process instance
              The Process that created the sample
        """

        ## Process that will create samples
        create_sample_process = expt.create_process_from_template("global_Primitive Crystal Structure")

        ## Create sample
        samples = create_sample_process.create_samples([sample_name])
        # Sample attributes (how to check names?):
        # "name"
        _add_string_measurement(create_sample_process, 'name', casm_proj.name)

        prim = casm_proj.prim

        # "lattice"
        #     "matrix"
        #     "parameters"
        #     "system" ("triclinic", "monoclinic", "orthorhombic", "tetragonal",
        #               "hexagonal", "rhombohedral", "cubic")
        #     "symmetry" (Schoenflies symbol)
        _add_numpy_matrix_measurement(
            create_sample_process,
            'lattice_matrix',
            prim.lattice_matrix)

        _add_vector_measurement(
            create_sample_process,
            'lattice_parameters',
            prim.lattice_parameters)

        _add_string_measurement(
            create_sample_process,
            'lattice_point_group_schonflies',
            prim.lattice_symmetry_s)

        _add_string_measurement(
            create_sample_process,
            'lattice_point_group_hermann_mauguin',
            prim.lattice_symmetry_hm)

        _add_string_measurement(
            create_sample_process,
            'lattice_system',
            prim.lattice_system)

        # "space_group"
        #      "point_group_schonflies"
        #      "point_group_hermann_mauguin"
        #      "number"
        #      "crystal_family" ("triclinic", "monoclinic", "orthorhombic",
        #                        "tetragonal", "hexagonal", "cubic")
        #      "crystal_system" ("triclinic", "monoclinic", "orthorhombic",
        #                        "tetragonal", "hexagonal", "trigonal", "cubic")
        _add_string_measurement(
            create_sample_process,
            'crystal_point_group_schonflies',
            prim.crystal_symmetry_s)

        _add_string_measurement(
            create_sample_process,
            'crystal_point_group_hermann_mauguin',
            prim.crystal_symmetry_hm)

        _add_string_measurement(
            create_sample_process,
            'crystal_family',
            prim.crystal_family)

        _add_string_measurement(
            create_sample_process,
            'crystal_system',
            prim.crystal_system)

        # right now, this is a string giving a range of possible values based on the
        #   crystal point group
        _add_string_measurement(
            create_sample_process,
            'space_group_number',
            prim.space_group_number)

        # "casm_prim_file"
        _add_file_measurement(create_sample_process, 'casm_prism_file', mcfile)

        # "elements" - currently only elemental components are allowed
        _add_list_measurement(
            create_sample_process,
            'elements',
            prim.elements,
            'string')

        # "n_elements"
        _add_integer_measurement(
            create_sample_process,
            'n_elements',
            len(prim.elements))

        # "components" - currently only elemental components are allowed
        _add_list_measurement(
            create_sample_process,
            'components',
            prim.components,
            'string')

        # "n_components"
        _add_integer_measurement(
            create_sample_process,
            'n_components',
            len(prim.components))

        # "n_independent_compositions"
        _add_integer_measurement(
            create_sample_process,
            'n_independent_compositions',
            prim.n_independent_compositions)

        # "degrees_of_freedom" ("occupation", "displacement", "strain")
        _add_string_measurement(
            create_sample_process,
            'degrees_of_freedom',
            prim.degrees_of_freedom)

        create_sample_process = expt.get_process_by_id(create_sample_process.id)

        return create_sample_process

    def mock_prim(self):
        return PrimMock()

class PrimMock(object):
    def __init__ (self):
        self.lattice_matrix = numpy.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]])
        self.lattice_parameters = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        self.lattice_symmetry_s = "tetragonal"
        self.lattice_symmetry_hm = 'D2h'
        self.lattice_system = 'D4h'
        self.crystal_symmetry_s = 'C4h'
        self.crystal_symmetry_hm = 'C4h'
        self.crystal_family = 'tetragonal'
        self.crystal_system = 'tetragonal'
        self.space_group_number = 'space_group'
        self.elements=['Al','NI']
        self.components=['Al','NI']
        self.n_independent_compositions = 5
        self.degrees_of_freedom = "displacement"


