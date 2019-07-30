import argparse
import difflib
import os
import sys

import materials_commons.api as mcapi
import materials_commons.cli.functions as clifuncs
from materials_commons.cli.print_formatter import PrintFormatter
from materials_commons.cli.functions import format_time, humanize, as_is

def make_version_record(data, index):
    return {
        "mtime": format_time(data["mtime"]),
        "size": humanize(data["size"]),
        "version": index,
        "id": data["id"],
        "checksum": data["checksum"]
    }

def make_versions(proj, path):
    """Make a list of versions records"""
    file = clifuncs.get_file_by_path(proj, path)

    if not file:
        print(p + ": No such file or directory on remote")
        exit(1)
    if isinstance(file, mcapi.Directory):
        print(p + ": Is a directory on remote")
        exit(1)
    if not isinstance(file, mcapi.File):
        print(p + ": Not a file on remote")
        exit(1)

    file = clifuncs.get_file_by_id(proj, file.input_data['id'])

    versions = []
    index = 0
    for vers in file.input_data["versions"]:
        versions.append(make_version_record(vers, index))
        index = index + 1

    vers = file.input_data
    versions.append(make_version_record(file.input_data, index))
    return versions

def list_versions(proj, path):
    versions = make_versions(proj, path)

    fmt = [
        ('mtime', 'mtime', '<', 24, as_is),
        ('size', 'size', '<', 8, as_is),
        ('id', 'id', '<', 36, as_is),
        ("checksum", "checksum", "<", 36, as_is),
        ("version", "version", "<", 8, as_is)
    ]

    pformatter = PrintFormatter(fmt)

    local_abspath = os.path.join(os.path.dirname(proj.local_path), path)
    print(os.path.relpath(local_abspath) + ":")
    pformatter.print_header()
    for vers in versions:
        pformatter.print(vers)

def version_as_str(proj, path, versions, vers_indicator):
    """Return version as str and standardized version name

    Arguments
    ---------
    path: str, File path
    versions: list of version records, output from `make_versions`
    vers_indicator: int or str,

    Returns
    -------
    (s, verspath):
        s: str, File version as a string
        verspath: str, Standardized version path
    """
    if vers_indicator == 'local':
        refpath = os.path.dirname(proj.local_path)
        local_abspath = os.path.join(refpath, path)
        if not os.path.exists(local_abspath):
            print(path + ": does not exist locally")
            exit(1)
        elif not os.path.isfile(local_abspath):
            print(path + ": is not a file locally")
            exit(1)
        versname = path + "-local"
        return (open(local_abspath, 'r').read(), versname)
    else:
        if vers_indicator == 'remote':
            vers_indicator = -1
        vers_indicator = int(vers_indicator)
        if vers_indicator < 0:
            vers_indicator = len(versions) + vers_indicator
        print("vers_indicator:", vers_indicator)
        versname = path + "-v" + str(vers_indicator)
        file_id = versions[vers_indicator]['id']
        return (clifuncs.download_file_as_string(proj.id, file_id, proj.remote), versname)

def print_version(proj, path, vers_indicator):
    """
    Arguments
    ---------
    proj: mcapi.Project
    path: str, path in project
    vers_indicator: str or int,
        Version number (positive or negative), or 'local', or 'remote' (=="-1")
    """
    versions = make_versions(proj, path)
    s, verspath = version_as_str(proj, path, versions, vers_indicator)
    refpath = os.path.dirname(proj.local_path)
    local_verspath = os.path.join(refpath, verspath)
    print(os.path.relpath(local_verspath) + ":")
    print(s)

def download_version(proj, path, vers_indicator):
    """
    Arguments
    ---------
    proj: mcapi.Project
    path: str, path in project
    vers_indicator: str or int
        Version number (positive or negative), or 'local', or 'remote' (=="-1")
    """
    versions = make_versions(proj, path)
    s, verspath = version_as_str(proj, path, versions, vers_indicator)

    refpath = os.path.dirname(proj.local_path)
    local_verspath = os.path.join(refpath, verspath)
    if os.path.exists(local_verspath):
        while True:
            print("Overwrite '" + os.path.relpath(local_verspath) + "'?")
            ans = input('y/n: ')
            if ans == 'y':
                break
            elif ans == 'n':
                return
    with open(local_verspath, 'w') as f:
        f.write(s)

def diff_versions(proj, path, vers_indicator_a, vers_indicator_b, method):
    """
    Arguments
    ---------
    proj: mcapi.Project
    path: str, path in project
    vers_indicator_a: str or int,
        Version number (positive or negative), or 'local', or 'remote' (=="-1") of 'from' file.
    vers_indicator_b: str or int,
        Version number (positive or negative), or 'local', or 'remote' (=="-1") of 'to' file.
    method: function,
        libdiff method to use to compare files
    """
    versions = make_versions(proj, path)
    s_a, verspath_a = version_as_str(proj, path, versions, vers_indicator_a)
    s_b, verspath_b = version_as_str(proj, path, versions, vers_indicator_b)

    refpath = os.path.dirname(proj.local_path)
    local_verspath_a = os.path.join(refpath, verspath_a)
    local_verspath_b = os.path.join(refpath, verspath_b)

    result = method(s_a.splitlines(keepends=True), s_b.splitlines(keepends=True), fromfile=os.path.relpath(local_verspath_a), tofile=os.path.relpath(local_verspath_b))
    sys.stdout.writelines(result)


def versions_subcommand(argv=sys.argv):
    """
    List, print, download, and compare file versions

    mc versions <pathspec>

    """
    parser = argparse.ArgumentParser(
        description='Get file versions',
        prog='mc versions')
    parser.add_argument('path', nargs=1, help='File to list versions of')
    parser.add_argument('-v', '--version', nargs="*", default=None, help='Select versions. Use \'local\' to compare with local version, \'remote\' to indicate latest remote version. Both positive and negative indices are accepted.')
    parser.add_argument('-p', '--print', action="store_true", default=False, help='Print selected version')
    parser.add_argument('--down', action="store_true", default=False, help='Download selected version')
    parser.add_argument('--diff', action="store_true", default=False, help='Compare selected versions')
    parser.add_argument('--context', action="store_true", default=False, help='Print diff using \'context diff\' method')

    # ignore 'mc ls'
    args = parser.parse_args(argv[2:])

    proj = clifuncs.make_local_project()
    pconfig = clifuncs.read_project_config()

    # convert cli input to materials commons path convention: <projectname>/path/to/file_or_dir
    refpath = os.path.dirname(proj.local_path)

    for p in args.path:
        local_abspath = os.path.abspath(p)
        path = os.path.relpath(local_abspath, refpath)

        if args.print:
            if len(args.version) != 1:
                print("--print requires 1 versions provided to -v,--version")
                exit(1)
            print_version(proj, path, args.version[0])
        elif args.down:
            if len(args.version) != 1:
                print("--down requires 1 versions provided to -v,--version")
                exit(1)
            download_version(proj, path, args.version[0])
        elif args.diff:
            if len(args.version) != 2:
                print("--diff requires 2 versions provided to -v,--version")
                exit(1)
            if args.context:
                method = difflib.context_diff
            else:
                method = difflib.unified_diff

            diff_versions(proj, path, args.version[0], args.version[1], method)
        else:
            list_versions(proj, path)


    return
