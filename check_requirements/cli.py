"""
check_requirements CLI Module

This module provides command-line interface (CLI) functions for managing Python package dependencies. It includes
functions for listing dependencies, checking for missing or extra packages, and raising errors for missing dependencies.

Functions:
    - list_deps(deps, sys_info): List dependencies to the console.
    - list_file(deps, sys_info, file_path): Save dependencies to a file.
    - check_missing(deps, file_deps, ignored_pkgs, sys_info): Check for missing dependencies and print a report.
    - check_extra(deps, file_deps, ignored_pkgs, sys_info): Check for extra dependencies and print a report.
    - raise_missing_error(deps, file_deps, ignored_pkgs, sys_info): Check for missing dependencies and raise an
    ImportError if found.
    - raise_extra_error(deps, file_deps, ignored_pkgs, sys_info): Check for extra dependencies and raise an ImportError
    if found.

Note:
    Use these functions in conjunction with command-line arguments to perform various actions on package dependencies.

Example:
    To list dependencies to the console:
    list_deps(deps, sys_info)

    To save dependencies to a file:
    list_file(deps, sys_info, "dependencies.txt")

    To check for missing dependencies and print a report:
    check_missing(deps, file_deps, ignored_pkgs, sys_info)

    To check for extra dependencies and print a report:
    check_extra(deps, file_deps, ignored_pkgs, sys_info)

    To check for missing dependencies and raise an ImportError if found:
    raise_missing_error(deps, file_deps, ignored_pkgs, sys_info)

    To check for extra dependencies and raise an ImportError if found:
    raise_extra_error(deps, file_deps, ignored_pkgs, sys_info)
"""

from .core import parse_deps_tree, filter_deps_tree, print_deps_tree, write_deps_tree_to_file, find_missing_pkgs, \
    check_and_raise_error


def list_deps(deps):
    """
    List dependencies to the console.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.

    Returns:
        None
    """
    print_deps_tree(deps)


def list_file(deps, file_path):
    """
    Save dependencies to a file.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        file_path (str): Path to the file where dependencies will be saved.

    Returns:
        None
    """
    write_deps_tree_to_file(file_path, deps)


def check_missing(deps, file_deps, ignored_pkgs):
    """
    Check for missing dependencies and print a report.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        file_deps (list): A list of hierarchical dictionaries representing file dependencies.
        ignored_pkgs (list): A list of packages to be ignored.

    Returns:
        None
    """
    missing_pkgs = find_missing_pkgs(deps, file_deps, ignored_pkgs)
    for pkg in missing_pkgs:
        print(f"Missing: {pkg['name']}{f''' == {pkg.get('version')}''' if pkg.get('version') else ''}")


def check_extra(deps, file_deps, ignored_pkgs):
    """
    Check for extra dependencies and print a report.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        file_deps (list): A list of hierarchical dictionaries representing file dependencies.
        ignored_pkgs (list): A list of packages to be ignored.

    Returns:
        None
    """
    extra_pkgs = find_missing_pkgs(file_deps, deps, ignored_pkgs)
    for pkg in extra_pkgs:
        print(f"Extra: {pkg['name']}{f''' == {pkg.get('version')}''' if pkg.get('version') else ''}")


def raise_missing_error(deps, file_deps, ignored_pkgs):
    """
    Check for missing dependencies and raise an ImportError if found.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        file_deps (list): A list of hierarchical dictionaries representing file dependencies.
        ignored_pkgs (list): A list of packages to be ignored.

    Returns:
        None
    """
    missing_pkgs = find_missing_pkgs(deps, file_deps, ignored_pkgs)
    if missing_pkgs:
        check_and_raise_error(deps, file_deps, ignored_pkgs)


def raise_extra_error(deps, file_deps, ignored_pkgs):
    """
    Check for extra dependencies and raise an ImportError if found.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        file_deps (list): A list of hierarchical dictionaries representing file dependencies.
        ignored_pkgs (list): A list of packages to be ignored.

    Returns:
        None
    """
    extra_pkgs = find_missing_pkgs(file_deps, deps, ignored_pkgs)
    if extra_pkgs:
        check_and_raise_error(file_deps, deps, ignored_pkgs)


def process_deps_file(dep_file, sys_info):
    with open(dep_file, "r", encoding="utf-8") as file:
        file_deps = parse_deps_tree(file.read())
        kwargs_len = len(
            {
                key: val for key, val in file_deps[0].items()
                if val is not None and key not in ["name", "at", "version", "deps"]
            }
        )
        if kwargs_len:
            file_deps = filter_deps_tree(file_deps, **sys_info)
        return file_deps
