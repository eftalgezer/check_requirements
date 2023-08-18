"""
Dependency Management Functions

This module provides functions for managing and analyzing Python package dependencies.

Functions:
 - get_list(): Returns a list of installed packages and their dependencies as text.
 - parse_deps_tree(lines: str): Parses the dependency tree from lines and returns a hierarchical dictionary.
 - add_info(deps: list): Adds Python version and system platform information to the dependency tree.
 - filter_deps_tree(deps: list, **kwargs): Filters the dependency tree based on provided keyword arguments.
 - ignore_pkgs(deps: list, ignored_pkgs: list): Ignores specified packages from the dependency tree.
 - print_deps_tree(deps: list, indent: int = 0): Prints the dependency tree to the console.
 - write_deps_tree_to_file(file_path: str, deps: dict, indent: int = 0): Writes the dependency tree to a file.
 - is_pkg_in_subtree(pkg: dict, deps: list): Checks if a package exists in a dependency subtree.
 - find_missing_pkgs(deps_a: list, deps_b: list): Finds missing packages in deps_a compared to
 deps_b.
 - check_and_raise_error(deps_a: list, deps_b: list): Raises ImportError if missing packages are
found in deps_a compared to deps_b.
 - update_reqs(file_path: str, deps: list, sys_info: dict = None, missing_pkgs: list = None, extra_pkgs: list = None):
 Updates the current requirements file based on provided missing and extra packages and system information.

 -  format_full_version(): Formats the Python interpreter's full version information.
"""
import io
import sys
from subprocess import Popen, PIPE
import shlex
import re


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
    deps (list): A hierarchical dictionary representing the dependency tree.

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
    return [pkg for pkg in deps if all(pkg.get(key) == val for key, val in kwargs.items() if pkg.get(key))]


def ignore_pkgs(deps, ignored_pkgs):
    """
    Ignores specified packages from the dependency tree.

    Args:
        deps (list): A list of hierarchical dictionaries representing the dependency tree.
        ignored_pkgs (list): A list of dictionaries where each dictionary contains "name" and "version" keys for
                            specifying ignored packages.

    Returns:
        list: The updated dependency tree with ignored packages removed.
    """
    updated_deps = []
    for pkg in deps:
        if not any(
                pkg["name"] == ignored["name"]
                and (
                        (pkg.get("at") == ignored.get("at")) if ignored.get("at") else True
                )
                and (
                        (pkg.get("version") == ignored.get("version")) if ignored.get("version") else True
                )
                for ignored in ignored_pkgs
        ):
            pkg_copy = pkg.copy()
            if pkg_copy["deps"]:
                pkg_copy["deps"] = ignore_pkgs(pkg_copy["deps"], ignored_pkgs)
            updated_deps.append(pkg_copy)
    return updated_deps


def print_deps_tree(deps, indent=0):
    """
    Prints the dependency tree to the console.

    Args:
    deps (list): A hierarchical dictionary representing the dependency tree.
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


def write_deps_tree_to_file(file_path, deps, mode="w"):
    """
    Writes the dependency tree to a file.

    Args:
    file_path (str): Path to the output file.
    deps (list): A hierarchical dictionary representing the dependency tree.
    mode (str): Writing mode.
    """
    original_stdout = sys.stdout
    with open(file_path, mode, encoding="utf-8") as sys.stdout:
        print_deps_tree(deps)
    sys.stdout = original_stdout


def is_pkg_in_subtree(pkg, deps):
    """
    Checks if a package exists in a dependency subtree.

    Args:
    pkg (dict): A dictionary representing the package to check.
    deps (list): A hierarchical dictionary representing the dependency tree.

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


def find_missing_pkgs(deps_a, deps_b):
    """
    Finds missing packages in deps_a compared to deps_b.

    Args:
    deps_a (list): A hierarchical dictionary representing the first dependency tree.
    deps_b (list): A hierarchical dictionary representing the second dependency tree.

    Returns:
    list: A list of missing packages.
    """

    missing_pkgs = []
    for pkg_a in deps_a:
        if not is_pkg_in_subtree(pkg_a, deps_b):
            missing_pkgs.append(pkg_a)
        missing_pkgs.extend(find_missing_pkgs(pkg_a["deps"], deps_b))
    return list({name["name"]: name for name in missing_pkgs}.values())


def check_and_raise_error(deps_a, deps_b):
    """
    Raises ImportError if missing packages are found in deps_a compared to deps_b.

    Args:
    deps_a (list): A hierarchical dictionary representing the first dependency tree.
    deps_b (list): A hierarchical dictionary representing the second dependency tree.

    Raises:
    ImportError: If missing packages are found.
    """

    missing_pkgs = find_missing_pkgs(deps_a, deps_b)
    if missing_pkgs:
        err_msg = "Missing packages:\n"
        for pkg in missing_pkgs:
            err_msg += f"{pkg['name']}{f''' == {pkg.get('version')}''' if pkg.get('version') else ''}\n"
        raise ImportError(err_msg)


def update_reqs(file_path, deps, sys_info=None, missing_pkgs=None, extra_pkgs=None):
    """
    Updates the current requirements file based on provided missing and extra packages and system information.

    Args:
    file_path (str): Path to the requirements file.
    deps (list): A list of hierarchical dictionaries representing the dependency tree.
    missing_pkgs (list): A list of missing packages to be updated in the requirements file.
    extra_pkgs (list): A list of extra packages to be removed from the requirements file.
    sys_info (dict) (optional): Dictionary containing system information to be added to the dependencies.

    Returns:
    None

    Raises:
    AttributeError: Neither missing_pkgs nor extra_pkgs is given.

    """
    if not any([missing_pkgs, extra_pkgs]):
        raise AttributeError("At least one of 'missing_pkgs' or 'extra_pkgs' should be given")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if missing_pkgs:
            lines = [line if all(
                re.search(rf"{re.escape(key)}\s*==\s*{re.escape(val)}", line)
                for key, val in sys_info.items()) else "here" for line in lines] \
                if sys_info \
                else ["here"]
            lines = list(set(lines))
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()
            print_deps_tree(deps)
            lines_to_insert = sys.stdout.getvalue().split("\n")
            sys.stdout = original_stdout
            for i, line in enumerate(lines_to_insert):
                lines.insert(lines.index("here") + i, line)
            lines = [line for line in lines if line != "here"]
        if extra_pkgs:
            for line in lines:
                pkg = parse_deps_tree(line)[0]
                if sys_info:
                    pkg = pkg \
                        if (all(key == val
                                for key in pkg if key not in ["name", "at", "version", "deps"])
                            for _, val in sys_info.values()) \
                        else None
                if pkg:
                    for extra_pkg in extra_pkgs:
                        if pkg["name"] == extra_pkg["name"] \
                                and pkg.get("at") == extra_pkg.get("at") \
                                and pkg.get("version") == extra_pkg.get("version"):
                            lines[lines.index(line)] = "remove"
                            break
            lines = [line for line in lines if line != "remove"]
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)


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
        version = f"{sys.implementation.version.major}" \
                  f".{sys.implementation.version.minor}" \
                  f".{sys.implementation.version.micro}"
        kind = sys.implementation.version.releaselevel
        if kind != "final":
            version += kind[0] + str(sys.implementation.version.serial)
        return version
    return "0"
