"""
This module contains tester functions for the various features provided by the check_requirements module.

The tester functions are designed to simulate specific test scenarios and assist in the unit testing of the main
functionality of check_requirements.
"""

import sys
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch
import pytest
from .helpers import _capture_stdout
from check_requirements import get_list, parse_deps_tree, add_info, filter_deps_tree, print_deps_tree, \
    print_deps_tree_with_info, write_deps_tree_to_file, write_deps_tree_with_info_to_file, is_pkg_in_subtree,\
    find_missing_pkgs, check_and_raise_error


def get_list_tester():
    """
    Tester function for get_list. Simulates listing dependencies.
    """
    return get_list()


def parse_deps_tree_tester(lines):
    """
    Tester function for parse_deps_tree. Simulates parsing dependency tree structures.
    """
    return parse_deps_tree(lines)


def add_info_tester(deps):
    """
    Tester function for add_info. Simulates adding Python version and system platform information to dependencies.
    """
    return add_info(deps)


def filter_deps_tree_tester(deps, **kwargs):
    """
    Tester function for filter_deps_tree.

    Args:
    deps (list): A list of hierarchical dictionaries representing the dependency tree.
    **kwargs: Keyword arguments for filtering the packages.

    Returns:
    list: The result of the filter_deps_tree function.
    """
    return filter_deps_tree(deps, **kwargs)


def print_deps_tree_tester(deps):
    """
    Tester function for print_deps_tree. Simulates printing the dependency tree structure.
    """
    return _capture_stdout(print_deps_tree, deps).split('\n')


def print_deps_tree_with_info_tester(deps, python_version, sys_platform):
    """
    Tester function for print_deps_tree_with_info. Simulates printing the dependency tree structure with added info.
    """
    return _capture_stdout(print_deps_tree_with_info, deps, python_version, sys_platform).split('\n')


def write_deps_tree_to_file_tester(deps):
    """
    Tester function for write_deps_tree_to_file. Simulates writing the dependency tree to a file.
    """
    written_lines = None
    with NamedTemporaryFile(delete=False) as temp_file:
        write_deps_tree_to_file(temp_file.name, deps)
        with open(temp_file.name, 'r') as f:
            written_lines = f.readlines()
    os.remove(temp_file.name)
    return written_lines


def write_deps_tree_with_info_to_file_tester(deps, python_version, sys_platform):
    """
    Tester function for write_deps_tree_with_info_to_file. Simulates writing the dependency tree with added info to a
    file.
    """
    written_lines = None
    with NamedTemporaryFile(delete=False) as temp_file:
        write_deps_tree_with_info_to_file(temp_file.name, deps, python_version, sys_platform)
        with open(temp_file.name, 'r') as f:
            written_lines = f.readlines()
    os.remove(temp_file.name)
    return written_lines


def is_pkg_in_subtree_tester(pkg, deps):
    """
    Tester function for is_pkg_in_subtree. Simulates checking if a package is present in a dependency subtree.
    """
    return is_pkg_in_subtree(pkg, deps)


def find_missing_pkgs_tester(deps_a, deps_b, ignored_pkgs):
    """
    Tester function for find_missing_pkgs. Simulates identifying missing packages between dependency trees.
    """
    return find_missing_pkgs(deps_a, deps_b, ignored_pkgs)


def check_and_raise_error_tester(deps_a, deps_b, ignored_pkgs):
    """
    Tester function for check_and_raise_error. Simulates checking and raising errors for missing or extra dependencies.
    """
    with pytest.raises(ImportError):
        check_and_raise_error(deps_a, deps_b, ignored_pkgs)


def main_tester(command):
    """
    Tester function for the main script. Simulates running the main script with specified command-line arguments.
    """
    from check_requirements.__main__ import main as rtmain
    with patch.object(sys, 'argv', command.split(" ")):
        return _capture_stdout(rtmain)
