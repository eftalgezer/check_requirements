"""
Dependency Management Functions

This module provides functions for managing and analyzing Python package dependencies.

Functions:
- get_list(): Returns a list of installed packages and their dependencies as text.
- parse_deps_tree(lines: str): Parses the dependency tree from lines and returns a hierarchical dictionary.
- add_info(deps: dict): Adds Python version and system platform information to the dependency tree.
- print_deps_tree(deps: dict, indent: int = 0): Prints the dependency tree to the console.
- print_deps_tree_with_info(deps: dict, python_version: str, sys_platform: str, indent: int = 0):
  Prints the dependency tree with version and platform info to the console.
- write_deps_tree_to_file(file_path: str, deps: dict, indent: int = 0): Writes the dependency tree to a file.
- write_deps_tree_with_info_to_file(file_path: str, deps: dict, python_version: str, sys_platform: str,
                                    indent: int = 0): Writes the dependency tree with info to a file.
- is_pkg_in_subtree(pkg: dict, deps: dict): Checks if a package exists in a dependency subtree.
- find_missing_pkgs(deps_a: dict, deps_b: dict, ignored_pkgs: list): Finds missing packages in deps_a
  compared to deps_b, ignoring specified packages.
- check_and_raise_error(deps_a: dict, deps_b: dict, ignored_pkgs: list): Raises ImportError if missing
  packages are found in deps_a compared to deps_b, ignoring specified packages.
"""

import sys
from subprocess import Popen, PIPE
import shlex


def get_list():
    """
    Fetches the list of installed packages and their dependencies.

    Returns:
    str: A formatted text containing the list of installed packages and their dependencies.
    """
    with Popen(shlex.split("pipdeptree -fl"), shell=False, stdout=PIPE) as command:
        lines = str(command.stdout.read())
        if "------------------------------------------------------------------------\n" in lines:
            lines = lines.split("------------------------------------------------------------------------\n")[-1]
        lines = lines.replace("b'", "").replace("'", "").replace("\\n", "\n")
    return lines


def parse_deps_tree(lines):
    """
    Parses the dependency tree from provided text lines.

    Args:
    lines (str): Text containing the formatted list of packages and their dependencies.

    Returns:
    list: A list of hierarchical dictionaries representing the dependency tree.
    """
    deps = []
    stack = []
    lines = lines.split("\n")
    lines.pop(-1)
    for line in lines:
        indent = line.count("  ")
        pkg_info = line.strip().split("==")
        pkg_name = None
        pkg_version = None
        if len(pkg_info) == 2:
            pkg_name, pkg_version = pkg_info[0], pkg_info[1]
        elif len(pkg_info) == 1:
            pkg_name, pkg_version = pkg_info[0], ""
        while len(stack) > indent:
            stack.pop()
        parent = stack[-1] if stack else None
        pkg_data = {
            "name": pkg_name,
            "version": pkg_version,
            "deps": [],
            "python_version": None,
            "sys_platform": None
        }
        if parent is not None:
            parent["deps"].append(pkg_data)
        else:
            deps.append(pkg_data)

        stack.append(pkg_data)

    return deps


def add_info(deps):
    """
    Adds Python version and system platform information to the dependency tree.

    Args:
    deps (dict): A hierarchical dictionary representing the dependency tree.

    Returns:
    list: The updated dependency tree with added information.
    """
    for pkg in deps:
        pkg["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}"
        pkg["sys_platform"] = sys.platform.lower()
        add_info(pkg["deps"])
    return deps


def print_deps_tree(deps, indent=0):
    """
    Prints the dependency tree to the console.

    Args:
    deps (dict): A hierarchical dictionary representing the dependency tree.
    indent (int, optional): Indentation level for formatting. Defaults to 0.
    """
    for pkg in deps:
        print("  " * indent + f"{pkg['name']}{'==' if pkg['version'] != '' else ''}{pkg['version']}")
        print_deps_tree(pkg['deps'], indent + 1)


def print_deps_tree_with_info(deps, python_version, sys_platform, indent=0):
    """
    Prints the dependency tree with version and platform info to the console.

    Args:
    deps (dict): A hierarchical dictionary representing the dependency tree.
    python_version (str): Python version information.
    sys_platform (str): System platform information.
    indent (int, optional): Indentation level for formatting. Defaults to 0.
    """
    for pkg in deps:
        print("  " * indent, end="")
        print(f"{pkg['name']}{'==' if pkg['version'] != '' else ''}{pkg['version']};", end=" ")
        print(f"python_version=={python_version} and sys_platform=={sys_platform}")
        print_deps_tree_with_info(pkg['deps'], python_version, sys_platform, indent + 1)


def write_deps_tree_to_file(file_path, deps):
    """
    Writes the dependency tree to a file.

    Args:
    file_path (str): Path to the output file.
    deps (dict): A hierarchical dictionary representing the dependency tree.
    """
    original_stdout = sys.stdout
    sys.stdout = open(file_path, "w", encoding="utf-8")
    print_deps_tree(deps)
    sys.stdout.close()
    sys.stdout = original_stdout


def write_deps_tree_with_info_to_file(file_path, deps, python_version, sys_platform):
    """
    Writes the dependency tree with version and platform info to a file.

    Args:
    file_path (str): Path to the output file.
    deps (dict): A hierarchical dictionary representing the dependency tree.
    python_version (str): Python version information.
    sys_platform (str): System platform information.
    """
    original_stdout = sys.stdout
    sys.stdout = open(file_path, "w", encoding="utf-8")
    print_deps_tree_with_info(deps, python_version, sys_platform)
    sys.stdout.close()
    sys.stdout = original_stdout


def is_pkg_in_subtree(pkg, deps):
    """
    Checks if a package exists in a dependency subtree.

    Args:
    pkg (dict): A dictionary representing the package to check.
    deps (dict): A hierarchical dictionary representing the dependency tree.

    Returns:
    bool: True if the package exists in the subtree, False otherwise.
    """
    for dep_pkg in deps:
        if (pkg["name"] == dep_pkg["name"] and
                pkg.get("version") == dep_pkg.get("version") and
                (not pkg.get("python_version") or pkg.get("python_version") == dep_pkg.get("python_version")) and
                (not pkg.get("sys_platform") or pkg.get("sys_platform") == dep_pkg.get("sys_platform"))):
            return True
        if is_pkg_in_subtree(pkg, dep_pkg["deps"]):
            return True
    return False


def find_missing_pkgs(deps_a, deps_b, ignored_pkgs):
    """
    Finds missing packages in deps_a compared to deps_b, ignoring specified packages.

    Args:
    deps_a (dict): A hierarchical dictionary representing the first dependency tree.
    deps_b (dict): A hierarchical dictionary representing the second dependency tree.
    ignored_pkgs (list): A list of packages to be ignored.

    Returns:
    list: A list of missing packages.
    """
    missing_pkgs = []
    for pkg_a in deps_a:
        pkg_name = pkg_a["name"]
        pkg_version = pkg_a.get("version")
        if any((pkg_name == ignored["name"] and pkg_version == ignored.get("version")) for ignored in
               ignored_pkgs):
            continue
        if not is_pkg_in_subtree(pkg_a, deps_b):
            missing_pkgs.append(pkg_a)
    return missing_pkgs


def check_and_raise_error(deps_a, deps_b, ignored_pkgs):
    """
    Raises ImportError if missing packages are found in deps_a compared to deps_b, ignoring specified packages.

    Args:
    deps_a (dict): A hierarchical dictionary representing the first dependency tree.
    deps_b (dict): A hierarchical dictionary representing the second dependency tree.
    ignored_pkgs (list): A list of packages to be ignored.

    Raises:
    ImportError: If missing packages are found.
    """
    missing_pkgs = find_missing_pkgs(deps_a, deps_b, ignored_pkgs)
    if missing_pkgs:
        err_msg = "Missing packages:\n"
        for pkg in missing_pkgs:
            err_msg += f"{pkg['name']}=={pkg.get('version', 'unknown')}\n"
        raise ImportError(err_msg)