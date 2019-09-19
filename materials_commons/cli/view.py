import argparse
import difflib
import os
import sys

import materials_commons.api as mcapi
import materials_commons.cli.functions as clifuncs


def view_subcommand(argv=sys.argv):
    """
    View objects

    mc view <view_id>

    """
    parser = argparse.ArgumentParser(
        description='View objects',
        prog='mc view')
    parser.add_argument('view_id', nargs=1, help='Object to view')

    # ignore 'mc ls'
    args = parser.parse_args(argv[2:])

    proj = clifuncs.make_local_project()
    viewstate = clifuncs.read_view_state()

    if args.view_id not in viewstate:
        print("Not found: " + args.view_id)
        exit(1)

    view_otype = args.view_id.split()[0]
    otype = None

    for key, value in clifuncs.VIEW_OTYPE.items():
        if view_otype == value:
            otype = key
            break

    if not otype:
        print("Not found: " + view_otype)
        exit(1)

    object = mcapi.get(object_id=viewstate[args.view_id], object_type=otype, remote=proj.remote)
    object.view(out=sys.stdout)

    # convert cli input to materials commons path convention: <projectname>/path/to/file_or_dir
    refpath = os.path.dirname(proj.local_path)

    for p in args.path:
        local_abspath = os.path.abspath(p)
        path = os.path.relpath(local_abspath, refpath)

        obj = clifuncs.get_by_path(proj, path)

        if not obj:
            print(p + ": No such file or directory on remote")
            exit(1)
        if isinstance(obj, mcapi.Directory):
            print(p + ": Is a directory on remote")
            exit(1)
        if not isinstance(obj, mcapi.File):
            print(p + ": Not a file on remote")
            exit(1)

        if not os.path.exists(local_abspath):
            print(local_abspath + ": No such file or directory locally")
            exit(1)
        if os.path.isdir(local_abspath):
            print(p + ": Is a directory locally")
            exit(1)
        if not os.path.isfile(local_abspath):
            print(p + ": Not a file locally")
            exit(1)

        remotefile = clifuncs.download_file_as_string(proj.id, obj.id, proj.remote)
        localfile = open(local_abspath, 'r').read()

        if args.context:
            method = difflib.context_diff
        else:
            method = difflib.unified_diff

        result = method(remotefile.splitlines(keepends=True), localfile.splitlines(keepends=True), fromfile="remote", tofile="local")
        sys.stdout.writelines(result)

    return
