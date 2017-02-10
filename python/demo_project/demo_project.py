from os import path as os_path
from mcapi import create_project, Template
from mcapi import list_projects
from mcapi import get_process_from_id


class DemoProject:
    def __init__(self,data_directory_path):
        self.build_data_directory = data_directory_path

    def build_project(self):
        project_name = "Demo Project"
        project_description = "A project for trying things out."
        experiment_name = "Microsegregation in HPDC L380"
        experiment_description = "A demo experiment -  A study of microsegregation in High Pressure Die Cast L380."
        processes_data = [
            {
                'name': 'Lift 380 Casting Day  # 1',
                'template':Template.create
            },
            {
                'name': 'Lift 380 Casting Day  # 1',
                'template': Template.sectioning
            },
            {
                'name': 'Casting L124',
                'template': Template.sectioning
            },
            {
                'name': 'Sectioning of Casting L124',
                'tempate': Template.EBSD_SEM_Data_Collection
            },
            {
                'name': 'EBSD SEM Data Collection - 5 mm plate',
                'template': Template.EBSD_SEM_Data_Collection
            },
            {
                'name': 'EPMA Data Collection - 5 mm plate - center',
                'template': Template.EPMA_Data_Collection
            }
        ]

        sample_names = [
            'l380', 'L124', 'L124 - 2mm plate', 'L124 - 3mm plate',
            'L124 - 5mm plate', 'L124 - 5mm plate - 3ST', 'L124 -tensil bar, gage'
        ]

        project = \
            self._get_or_creaet_project(project_name, project_description)
        experiment = \
            self._get_or_create_experiment(project, experiment_name, experiment_description)

        processes = []
        for entry in processes_data:
            process_name = entry['name']
            template = entry['template']
            process = self._get_or_create_process(experiment,process_name,template)
            processes.append(process)

        samples = []
        samples.append(
            self._get_or_create_output_sample_from_process(
                processes[0], sample_names[0:1]
            )
        )
        samples.append(
            self._get_or_create_output_sample_from_process(
                processes[1], sample_names[1:2]
            )
        )

        samples.append(
            self._get_or_create_output_sample_from_process(
                processes[2], sample_names[2:]
            )
        )

    # Support methods

    def _get_or_create_project(self, project_name, project_description):
        projects = list_projects()
        project = None
        for p in projects:
            if p.name == project_name:
                project = p
        if not project:
            project = create_project(
                name=project_name,
                description=project_description)
        return project

    def _get_or_create_experiment(self, project, experiment_name,experiment_description):
        experiments = project.fetch_experiments()
        experiment = None
        for ex in experiments:
            if (ex.name == experiment_name):
                experiment = ex
        if not experiment:
            experiment = project.create_experiment(
                name=experiment_name,
                description=experiment_description)
        return experiment

    def _get_or_create_process(self, experiment, process_name, template_id):
        experiment = experiment.fetch_and_add_processes()
        processes = experiment.processes
        selected_process = None
        for process in processes:
            if template_id == process.template_id and process_name == process.name:
                selected_process = process
        process = selected_process
        if not process:
            process = experiment.create_process_from_template(Template.create)
            process.add_name(process_name)
        return process

    def _get_or_create_output_sample_from_process(self, process, sample_names):
        samples = process.output_samples
        selected_samples = []
        for sample in samples:
            if sample.name in sample_names:
                selected_samples.append(sample)
        samples = selected_samples
        if not samples:
            samples = create_sample_process.create_samples(
                sample_names=sample_names
            )
        return samples



'''
        filepath_for_sample = self._make_data_dir_path('sem.tif')
        directory_path = "/FilesForSample"
        filename_for_sample = "SampleFile.tif"
        sample_file = self._get_file_from_project(project, directory_path, filename_for_sample)
        if not sample_file:
            sample_file = project.add_file_using_directory(
                project.add_directory(directory_path),
                filename_for_sample,
                filepath_for_sample
            )

        create_sample_process = get_process_from_id(project, experiment, create_sample_process.id)
        if not self._process_has_file(create_sample_process, sample_file):
            create_sample_process.add_files([sample_file])
            create_sample_process = get_process_from_id(project, experiment, create_sample_process.id)

        measurement_data = {
            "name": "Composition",
            "attribute": "composition",
            "otype": "composition",
            "unit": "at%",
            "value": [
                {"element": "Al", "value": 94},
                {"element": "Ca", "value": 1},
                {"element": "Zr", "value": 5}],
            "is_best_measure": True
        }
        measurement = create_sample_process.create_measurement(data=measurement_data)
        measurement_property = {
            "name": "Composition",
            "attribute": "composition"
        }
        create_sample_process_updated = \
            create_sample_process.set_measurements_for_process_samples(
                measurement_property, [measurement])
        measurement_out = create_sample_process_updated.measurements[0]
        composition = measurement_out
        value_list = composition.value

        return (project, experiment)
'''

'''
    def _get_file_from_project(self, project, directory_path, filename):
        directory = project.get_directory(directory_path)
        children = directory.get_children()
        selected_file = None
        for entry in children:
            if entry.otype == 'file' and entry.name == filename:
                selected_file = entry
        return selected_file

    def _process_has_file(self, process, file):
        selected_file = None
        for check_file in process.files:
            if check_file.id == file.id:
                selected_file = check_file
        return selected_file

    def _make_data_dir_path(self, file_name):
        test_file = os_path.join(self.build_data_directory, file_name)
        return test_file

'''