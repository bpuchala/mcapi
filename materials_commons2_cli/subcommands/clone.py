import argparse
import json
import os
import sys

import materials_commons2 as mcapi
import materials_commons2_cli.functions as clifuncs

def clone_subcommand(argv=sys.argv):
    """
    'Clone' a project, i.e. set the local directory tree where files should
    be uploaded/downloaded. Creates a '.mc/config.json'.

    mc clone <projid> [--remote <remotename>]

    """
    parser = argparse.ArgumentParser(
        description='Clone an existing project',
        prog='mc clone')
    parser.add_argument('id', help='Project id')
    clifuncs.add_remote_option(parser, 'Remote to clone project from')

    # ignore 'mc clone'
    args = parser.parse_args(argv[2:])

    # get remote, from command line option or default
    remote_config = clifuncs.optional_remote_config(args)

    project_id = args.id
    parent_dest = os.getcwd()
    proj = clifuncs.clone_project(remote_config, project_id, parent_dest)

    # done
    print("Cloned project from", remote_config.mcurl, "to", proj.local_path)
    clifuncs.print_projects([proj])
