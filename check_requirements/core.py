"""
Dependency Management Functions

This module provides functions for managing and analyzing Python package dependencies.

Functions:
 - get_list(): Returns a list of installed packages and their dependencies as text.
 - parse_deps_tree(lines: str): Parses the dependency tree from lines and returns a hierarchical dictionary.
 - add_info(deps: dict): Adds Python version and system platform information to the dependency tree.
 - filter_deps_tree(deps, **kwargs): Filters the dependency tree based on provided keyword arguments.
 - print_deps_tree(deps: dict, indent: int = 0): Prints the dependency tree to the console.
 - write_deps_tree_to_file(file_path: str, deps: dict, indent: int = 0): Writes the dependency tree to a file.
 - is_pkg_in_subtree(pkg: dict, deps: dict): Checks if a package exists in a dependency subtree.
 - find_missing_pkgs(deps_a: dict, deps_b: dict, ignored_pkgs: list): Finds missing packages in deps_a compared to
 deps_b, ignoring specified packages.
 - check_and_raise_error(deps_a: dict, deps_b: dict, ignored_pkgs: list): Raises ImportError if missing packages are
found in deps_a compared to deps_b, ignoring specified packages.
 -  format_full_version(): Formats the Python interpreter's full version information.
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
        lines = command.stdout.read()
        lines = lines.decode("utf-8")
        if "------------------------------------------------------------------------\n" in lines:
            lines = lines.split("------------------------------------------------------------------------\n")[-1]
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
    if lines[-1].strip() == "":
        lines.pop(-1)
    for line in lines:
        indent = line.count("  ")
        info = line.split(";")
        pkg_info = info[0].strip().split("==")
        pkg_name = None
        pkg_at = None
        pkg_version = None
        if len(pkg_info) == 2:
            pkg_name, pkg_version = pkg_info[0].strip(), pkg_info[1].strip()
        elif len(pkg_info) == 1:
            pkg_name, pkg_version = pkg_info[0], None
        if "@" in pkg_name:
            pkg_name = pkg_name.split("@")
            pkg_at = pkg_name[1].strip()
            pkg_name = pkg_name[0].strip()
        while len(stack) > indent:
            stack.pop()
        parent = stack[-1] if stack else None
        pkg_data = {"name": pkg_name}
        if pkg_version:
            pkg_data["version"] = pkg_version
        if pkg_at:
            pkg_data["at"] = pkg_at
        if len(info) == 2:
            sys_info = info[1].split(" and ")
            sys_info = [var.strip().split("==") for var in sys_info]
            for var in sys_info:
                pkg_data[var[0].strip()] = var[1].strip()
        pkg_data["deps"] = []
        if parent is not None:
            parent["deps"].append(pkg_data)
        else:
            deps.append(pkg_data)
        stack.append(pkg_data)
    return deps


def add_info(deps, **kwargs):
    """
    Adds given system information to the dependency tree.

    Args:
    deps (dict): A hierarchical dictionary representing the dependency tree.

    Returns:
    list: The updated dependency tree with added information.
    """
    for pkg in deps:
        keys = list(pkg)
        new_pkg = pkg.copy()
        for key, val in kwargs.items():
            keys.insert(keys.index("deps"), key)
            new_pkg[key] = val
        index = deps.index(pkg)
        deps[index] = {key_key: new_pkg[key_key] for key_key in keys}
        deps[index]["deps"] = add_info(pkg["deps"], **kwargs)
    return deps


def filter_deps_tree(deps, **kwargs):
    """
    Filters the dependency tree based on provided keyword arguments.

    This function filters the dependency tree to include only packages that match the specified criteria
    provided as keyword arguments. Each keyword argument should correspond to a key-value pair in the package
    dictionary. Only packages that match all the specified criteria will be included in the result.

    Args:
    deps (list): A list of hierarchical dictionaries representing the dependency tree.
    **kwargs: Keyword arguments for filtering the packages. Each keyword argument should correspond to a key-value
        pair in the package dictionary.

    Returns:
    list: A filtered list of packages that match the specified criteria.
    """
    return [pkg for pkg in deps if all(pkg.get(key) == val for key, val in kwargs.items())]


def print_deps_tree(deps, indent=0):
    """
    Prints the dependency tree to the console.

    Args:
    deps (dict): A hierarchical dictionary representing the dependency tree.
    indent (int, optional): Indentation level for formatting. Defaults to 0.
    """
    for pkg in deps:
        print("  " * indent, end="")
        semicolon = True
        for count, (key, val) in enumerate(pkg.items(), start=1):
            if key == "name":
                print(val, end="")
            if key == "at" and val:
                print(f" @ {val}", end="")
            if key == "version" and val:
                print(f" == {val}", end="")
            if key not in ["name", "at", "version", "deps"] and val:
                if semicolon:
                    print(";", end=" ")
                    semicolon = False
                print(f"{key} == {val}", end=" and " if count != len(pkg.items()) - 1 else "")
            if key == "deps":
                print("")
                print_deps_tree(pkg["deps"], indent + 1)


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
        if (
                pkg["name"] == dep_pkg["name"]
                and (
                (pkg.get("version") == dep_pkg.get("version"))
                if pkg.get("version") and dep_pkg.get("version") else True)
        ):
            return True
        if is_pkg_in_subtree(pkg, dep_pkg["deps"]):
            return True
    return False


def find_missing_pkgs(deps_a, deps_b, ignored_pkgs=None):
    """
    Finds missing packages in deps_a compared to deps_b, ignoring specified packages.

    Args:
    deps_a (dict): A hierarchical dictionary representing the first dependency tree.
    deps_b (dict): A hierarchical dictionary representing the second dependency tree.
    ignored_pkgs (list): A list of packages to be ignored.

    Returns:
    list: A list of missing packages.
    """
    if not ignored_pkgs:
        ignored_pkgs = []
    missing_pkgs = []
    for pkg_a in deps_a:
        pkg_name = pkg_a["name"]
        pkg_version = pkg_a.get("version")
        if \
                any(
                    pkg_name == ignored["name"] and
                    ((pkg_version == ignored.get("version")) if ignored.get("version") else True)
                    for ignored in ignored_pkgs
                ):
            missing_pkgs.extend(find_missing_pkgs(pkg_a["deps"], deps_b, ignored_pkgs))
        elif not is_pkg_in_subtree(pkg_a, deps_b):
            missing_pkgs.append(pkg_a)
        missing_pkgs.extend(find_missing_pkgs(pkg_a["deps"], deps_b, ignored_pkgs))
    return list({name["name"]: name for name in missing_pkgs}.values())


def check_and_raise_error(deps_a, deps_b, ignored_pkgs=None):
    """
    Raises ImportError if missing packages are found in deps_a compared to deps_b, ignoring specified packages.

    Args:
    deps_a (dict): A hierarchical dictionary representing the first dependency tree.
    deps_b (dict): A hierarchical dictionary representing the second dependency tree.
    ignored_pkgs (list): A list of packages to be ignored.

    Raises:
    ImportError: If missing packages are found.
    """
    if not ignored_pkgs:
        ignored_pkgs = []
    missing_pkgs = find_missing_pkgs(deps_a, deps_b, ignored_pkgs)
    if missing_pkgs:
        err_msg = "Missing packages:\n"
        for pkg in missing_pkgs:
            err_msg += f"{pkg['name']}{f''' == {pkg.get('version')}''' if pkg.get('version') else ''}\n"
        raise ImportError(err_msg)


def format_full_version():
    """
    Formats the Python interpreter's full version information.

    This function retrieves the full version information of the Python interpreter and formats it into a string.
    The formatted version includes the major, minor, and micro version numbers. If the interpreter's release level
    is not 'final', the release level and serial number are also included in the formatted version string.

    Returns:
    str: A formatted string representing the Python interpreter's full version information.
    """
    if hasattr(sys, "implementation"):
        version = "{0.major}.{0.minor}.{0.micro}".format(sys.implementation.version)
        kind = sys.implementation.version.releaselevel
        if kind != "final":
            version += kind[0] + str(sys.implementation.version.serial)
        return version
    return "0"
