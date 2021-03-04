"""This script runs mypy on all py files in the given directory.

Author: Shining (Fred) Lou
"""
import os
import sys
import subprocess
from typing import List, Tuple


def get_src_file_list(dir: str) -> List[str]:
    """ Get all py files from the given directories
    """
    res = []
    for root, dirs, files in os.walk(dir):
        dirs.sort()
        for file_name in sorted(files):
            if file_name[-3:] != '.py': continue
            full_path = os.path.join(root, file_name)
            if full_path != './typecheck.py':
                res.append(full_path)
    return res


def run_mypy(files: List[str] = []):
    """ Call mypy given list of files, packages, modules and arguments
    Output: stdout, stderr
    """

    args = ['mypy', '--follow-imports', 'silent', '--ignore-missing-imports', '--check-untyped-defs', '--sqlite-cache',
            '--show-error-codes']
    command = args + files
    print(command)
    subprocess.run(command)


def process_duplicates(files: List[str]):
    file_name_set = set()
    duplicate_set = set()
    for file in files:
        file_split = file.split("/")
        file_name = file_split[len(file_split) - 1]
        if file_name not in file_name_set:
            file_name_set.add(file_name)
        else:
            duplicate_set.add(file_name)
    base_file_list = []
    duplicate_file_list = []
    for file in files:
        file_split = file.split("/")
        file_name = file_split[len(file_split) - 1]
        if file_name not in duplicate_set:
            base_file_list.append(file)
        else:
            duplicate_file_list.append(file)
    return base_file_list,duplicate_file_list


def main() -> None:
    print('===============START OF MYPY===============')
    src_files = get_src_file_list('.')
    base_file_list, duplicate_file_list = process_duplicates(src_files)

    python_version = '{}.{}'.format(sys.version_info.major, sys.version_info.minor)
    os.mkdir('mypy_test_cache')

    run_mypy(base_file_list)
    os.rename('./.mypy_cache/{}/cache.db'.format(python_version), './mypy_test_cache/main_cache.db')
    i = 0
    for dup_file in duplicate_file_list:
        run_mypy([dup_file])
        os.rename('./.mypy_cache/{}/cache.db'.format(python_version), './mypy_test_cache/duplicate_cache({}).db'.format(i))
        i += 1
    print('===============END OF MYPY===============')


if __name__ == '__main__':
    main()