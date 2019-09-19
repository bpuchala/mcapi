import json
import os
import requests
import sys

from materials_commons.cli.list_objects import ListObjects
import materials_commons.api as mcapi
import materials_commons.cli.functions as clifuncs

from ..api import __api as mc_raw_api

def add_files_to_process(project_id, process_id, files, remote=None):
    """
    Arguments
    ---------
    project_id: str, Project ID
    process_id: str, Process ID
    files: list of objects

        Ex: files: [
                {"file_id":<id>, "direction": <'in', 'out', or ''>},
                ...
            ]

    Notes
    -----
    If file direction == 'in' or 'out', then the file is included in both 'files' and 'input_files' or 'output_files', respectively.

    If file direction == '' (empty string), then the file is only included in 'files'.

    """
    result = clifuncs.post_v3(
        "addFilesToProcess",
        {
            'project_id': project_id,
            'process_id': process_id,
            'files': [{'file_id':id, 'direction':''} for id in file_ids]
        },
        remote=remote,
        use_data=True)
    return mcapi.Process(result['data'])

def remove_files_from_process(project_id, process_id, file_ids, remote=None):
    """
    Arguments
    ---------
    project_id: str, Project ID
    process_id: str, Process ID
    file_ids: list of str, List of File IDs

    Notes
    -----
    Files are stored with a direction, one of 'in', 'out', or '' (empty string). A file with
    direction 'in' or 'out' is listed both in "input_files" and "files", or "output_files"
    and "files", respectively. Removing a file removes it from all lists.
    """
    result = clifuncs.post_v3(
        "removeFilesFromProcess",
        {
            'project_id': project_id,
            'process_id': process_id,
            'files': file_ids
        },
        remote=remote)
    print(json.dumps(result['data'], indent=2))
    return mcapi.Process(result['data'])

def get_related_samples(processes):
    # get related samples and add those
    samples_by_id = {}
    for proc in processes:
        for samp in proc.input_samples:
            samples_by_id[samp.id] = samp
        for samp in proc.output_samples:
            samples_by_id[samp.id] = samp
    samples = [value for key,value in samples_by_id.items()]
    return samples


class ProcSubcommand(ListObjects):

    def __init__(self):
        super(ProcSubcommand, self).__init__(
            ["proc"], "Process", "Processes", expt_member=True,
            list_columns=['name', 'owner', 'template_name', 'id', 'mtime'],
            creatable=True,
            deletable=True,
            custom_selection_actions=['link_files', 'use_files', 'create_files', 'unlink_files', 'add_to_dataset', 'remove_from_dataset', 'create_dataset'],
            request_confirmation_actions={
                'add_to_dataset': 'Are you sure you want to add these processes to the dataset?',
                'remove_from_dataset': 'Are you sure you want to remove these processes from the dataset?',
                'create_dataset': 'Create a new dataset with these processes?'
            }
        )

    def get_all_from_experiment(self, expt):
        return expt.get_all_processes()

    def get_all_from_project(self, proj):
        return proj.get_all_processes()

    def list_data(self, obj):
        return {
            'name': clifuncs.trunc(obj.name, 40),
            'owner': obj.owner,
            'template_name': obj.template_name,
            'id': obj.id,
            'mtime': clifuncs.format_time(obj.mtime)
        }

    def print_details(self, obj, out=sys.stdout):
        obj.pretty_print(shift=0, indent=2, out=out)

    def create(self, args, out=sys.stdout):
        """Create new process

        Using:
            mc proc <proc_name> [--desc <description>] [--ptype <proc type>] --create
            mc proc --name <proc_name> [--desc <description>] [--ptype <proc type>] --create
        """
        from materials_commons.api.mc_object_utility import make_object

        proj = clifuncs.make_local_project()

        in_names = []
        if args.expr:
            in_names += args.expr
        if args.name:
            in_names += [args.name]

        if len(in_names) != 1:
            print('create one process at a time')
            print('example: mc proc ProcName --create')
            parser.print_help()
            exit(1)

        expt = clifuncs.make_local_expt(proj)
        if args.template:
            # if you use a template:
            #   template_id = arg.template
            #   template_name = <template name is template_id excluding the 'global_' prefix>
            #   ptype = template_name
            #   process_type = from template: one of "create"/"transform"/"measurement"/"analysis"
            result = mc_raw_api.create_process_from_template(proj.id, expt.id, args.template, remote=proj.remote)
            process = mcapi.Process(result)
        else:
            # TODO: make createProcess more flexible
            #
            # if you don't use a template:
            #   template_id = "global_Generic Transform Samples Template"
            #   template_name = <template name is template_id excluding the 'global_' prefix>
            #   ptype = <same as process name> NOTE: confusingly, this is passed as 'process_type'
            #   process_type = "transform"
            process = mcapi.create_process(proj.id, experiment_id=expt.id, ptype=args.ptype)
            pass

        # resulting_objects = []
        # for name in in_names:
        #     dataset = mcapi.create_dataset(proj.id, name, description=args.desc, remote=proj.remote)
        #     print('Created dataset:', dataset.id)
        #     resulting_objects.append(dataset)
        # self.output(resulting_objects, args, out=out)
        return

    def delete(self, objects, args, dry_run, out=sys.stdout):
        if dry_run:
            out.write('Dry-run is not yet possible when deleting processes.\n')
            out.write('Aborting\n')
            return
        for obj in objects:
            # if getattr(obj, 'experiment', None) is None:
            #     out.write('Could not delete processes.\n')
            #     out.write('Currently, processes must be deleted via an experiment.\n')
            #     out.write('Please include the --expt option.\n')
            #     out.write('Aborting\n')
            #     return

            try:
                result = obj.delete()
            except requests.exceptions.HTTPError as e:
                try:
                    print(e.response.json()['error'])
                except:
                    print("  FAILED, for unknown reason")
                result = None

            if result is None:
                out.write('Could not delete process: ' + obj.name + ' ' + obj.id + '\n')
                out.write('At present, a process can not be deleted via the mcapi if ')
                out.write('any of the following are true: \n')
                out.write('  (1) it is not a leaf node in the workflow,\n')
                out.write('  (2) is is in a dataset, \n')
                out.write('  (3) it is a create sample (type) process with one or more output samples.\n')
            else:
                out.write('Deleted process: ' + obj.name + ' ' + obj.id + '\n')

    def add_custom_options(self, parser):

        # for --create and --clone, set dataset name, description
        parser.add_argument('--desc', type=str, default="", help='Create or add description, for use with --create, --clone, or --create-dataset.')
        parser.add_argument('--name', type=str, default="", help='New process, for use with --create or --clone.')
        parser.add_argument('--ptype', type=str, default="", help='Specify a custom process type, for use with --create or --clone.')
        parser.add_argument('--template', type=str, default="", metavar="TEMPLATE_ID", help='Specify a process template, for use with --create or --clone. Must be a template id.')

        # --clone
        parser.add_argument('--clone', action="store_true", default=False, help='Clone the selected process. Only allowed for a single process.')


        # linking files
        parser.add_argument('--link-files', nargs="*", help='List of files to link to selected processes.')
        parser.add_argument('--use-files', nargs="*", help='List of input files to link to selected processes.')
        parser.add_argument('--create-files', nargs="*", help='List of output files to link to selected processes.')
        parser.add_argument('--unlink-files', nargs="*", help='List of files to unlink from selected processes.')

        # dataset operations
        parser.add_argument('--add-to-dataset', type=str, default="", metavar='DATASET_ID', help='Add selected processes to the dataset with given ID.')
        parser.add_argument('--remove-from-dataset', type=str, default="", metavar='DATASET_ID', help='Remove selected processes from the dataset with given ID.')
        parser.add_argument('--create-dataset', type=str, default="", metavar='DATASET_NAME', help='Create a new dataset with the selected processes.')

    def _link_files(self, objects, args, files, direction=None, out=sys.stdout):
        """Link files to processes (any direction)"""
        if direction is None:
            print("Error using _link_files: no direction provided")
        elif direction not in ['in', 'out', '']:
            print("Error using _link_files: unsupported direction: '" + direction + "'")

        proj = clifuncs.make_local_project()

        if not files:
            print("No files")
            return

        # convert cli input to materials commons path convention: <projectname>/path/to/file_or_dir
        refpath = os.path.dirname(proj.local_path)
        paths = [os.path.relpath(os.path.abspath(p), refpath) for p in files]
        files = [clifuncs.get_file_by_path(proj, p) for p in paths]
        file_ids = [file.id for file in files]

        resulting_objects = []
        for obj in objects:
            try:
                files = [{"file_id":id, "direction":direction} for id in file_ids]
                resulting_objects.append(add_files_to_process(proj.id, obj.id, files, proj.remote))
            except requests.exceptions.HTTPError as e:
                try:
                    print(json.dumps(e.response.json(), indent=2))
                    print(e.response.json()["error"])
                except:
                    print("  FAILED, for unknown reason")
                return False
        self.output(resulting_objects, args, out=out)
        return

    def link_files(self, objects, args, out=sys.stdout):
        """Link files to processes (direction == '')

        Using:
            mc proc --id <proc_id> --link-files <file1> ...
            mc proc <process_name_search> --link-files <file1> ...
        """
        self._link_files(objects, args, args.link_files, direction='', out=out)

    def use_files(self, objects, args, out=sys.stdout):
        """Link files 'used by' processes (direction == 'in')

        Using:
            mc proc --id <proc_id> --use-files <file1> ...
            mc proc <process_name_search> --use-files <file1> ...
        """
        self._link_files(objects, args, args.use_files, direction='in', out=out)

    def create_files(self, objects, args, out=sys.stdout):
        """Link files 'created by' processes (direction == 'out')

        Using:
            mc proc --id <proc_id> --create-files <file1> ...
            mc proc <process_name_search> --create-files <file1> ...
        """
        self._link_files(objects, args, args.create_files, direction='out', out=out)

    def unlink_files(self, objects, args, out=sys.stdout):
        """Unlink files to processes

        Using:
            mc proc --id <proc_id> --unlink-files <file1> ...
            mc proc <process_name_search> --unlink-files <file1> ...
        """
        proj = clifuncs.make_local_project()

        if not args.unlink_files:
            print("No files")
            return

        # convert cli input to materials commons path convention: <projectname>/path/to/file_or_dir
        refpath = os.path.dirname(proj.local_path)
        paths = [os.path.relpath(os.path.abspath(p), refpath) for p in args.unlink_files]
        files = [clifuncs.get_file_by_path(proj, p) for p in paths]
        file_ids = [file.id for file in files]

        resulting_objects = []
        for obj in objects:
            try:
                resulting_objects.append(remove_files_from_process(proj.id, obj.id, file_ids, proj.remote))
            except requests.exceptions.HTTPError as e:
                try:
                    print(json.dumps(e.response.json(), indent=2))
                    print(e.response.json()["error"])
                except:
                    print("  FAILED, for unknown reason")
                return False
        self.output(resulting_objects, args, out=out)
        return

    def add_to_dataset(self, objects, args, out=sys.stdout):
        """Add processes to a dataset

        Currently, the backend only supports adding samples to a dataset. This function finds samples related to the selected processes and adds those.
        """

        proj = clifuncs.make_local_project()
        dataset_id = args.add_to_dataset

        print("\nCurrently, Materials Commons only supports adding samples to a dataset.")
        print("Identifying related samples...")
        samples = get_related_samples(objects)

        if not args.force:

            # use SampSubcommand to print related samples
            from .samp import SampSubcommand
            samp_command = SampSubcommand()
            samp_command.output(samples, args, out=out)

            msg = "Are you sure you want to add these samples to the dataset?"

            print("")
            if not clifuncs.request_confirmation(msg):
                out.write("Aborting\n")
                return

        sample_ids = [samp.id for samp in samples]
        dataset = mcapi.add_samples_to_dataset(proj.id, dataset_id, sample_ids=sample_ids, remote=proj.remote)

        #TODO
        print("Warning: Related processes are not currently being added to the dataset along with the samples.")
        print("To clone a new dataset that updates the processes based on the current samples, use:")
        print("    mc dataset --proj --id " + dataset.id + " --clone --refresh-processes")

        return

    def remove_from_dataset(self, objects, args, out=sys.stdout):
        """Remove processes from a dataset"""

        print("--remove-from-dataset is under construction")
        exit(1)

        # TODO: backend issue is causing this to fail
        proj = clifuncs.make_local_project()
        dataset_id = args.remove_from_dataset
        dataset = mcapi.remove_processes_from_dataset(proj.id, dataset_id, [proc.id for proc in objects], remote=proj.remote)

        return

    def create_dataset(self, objects, args, out=sys.stdout):
        """Create a dataset with the selected processes"""
        print("--create-dataset is under construction")
        exit(1)

        proj = clifuncs.make_local_project()
        dataset_name = args.create_dataset
        dataset_desc = ""
        if args.desc:
            dataset_desc = args.desc
        dataset = mcapi.create_dataset(proj.id, dataset_name, dataset_desc, sample_ids=[samp.id for samp in objects], remote=proj.remote)

        return
