import unittest
from random import randint
from mcapi import Project
from mcapi import get_all_projects
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestProject(unittest.TestCase):

    # TODO: this is a race condition - it could fail! - create precondition that there is at least one project!
    def test_list_projects_object(self):
        projects = get_all_projects()
        project = projects[0]
        self.assertIsNotNone(project.name)
        self.assertTrue(isinstance(project, Project))
        self.assertIsNotNone(project.description)
        self.assertIsNotNone(project.id)
        self.assertNotEqual(project.name, "")

    def test_create_project_object(self):
        name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        project = create_project(name, description)
        self.assertIsNotNone(project.name)
        self.assertTrue(isinstance(project, Project))
        self.assertIsNotNone(project.description)
        self.assertIsNotNone(project.id)
        self.assertNotEqual(project.name, "")
        self.assertEqual(name, project.name)
        self.assertEqual(description, project.description)
