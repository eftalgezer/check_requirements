"""
check_requirements terminal client

This script provides a command-line interface for managing Python package dependencies. It offers various features
such as listing dependencies, checking for missing or extra packages, and raising errors for missing dependencies.

Usage:
    python __main__.py [options]

Options:
    --list, -l                List dependencies to the console.
    --list-file FILE, -lf FILE
                              Save dependencies to a file.
    --check-missing FILE, -cm FILE
                              Check for missing dependencies and print a report.
    --check-extra FILE, -ce FILE
                              Check for extra dependencies and print a report.
    --raise-missing-error, -rme
                              Check for missing dependencies and raise an ImportError if found.
    --raise-extra-error, -ree Check for extra dependencies and raise an ImportError if found.
    --ignore FILE, -i FILE    Path to a file containing ignored packages.
    --ignore-packages PKG [PKG ...], -ip PKG [PKG ...]
                              List of packages to ignore.
    --with-info               Include Python version and OS information when listing dependencies.

Note:
    Use appropriate options to perform desired actions on package dependencies.

Examples:
    List dependencies to the console:
    check_dependencies --list

    Save dependencies to a file:
    check_dependencies --list-file dependencies.txt

    Check for missing dependencies and print a report:
    check_dependencies --check-missing missing_deps.txt

    Check for extra dependencies and print a report:
    check_dependencies --check-extra extra_deps.txt

    Check for missing dependencies and raise an error if found:
    check_dependencies --raise-missing-error missing_deps.txt

    Check for extra dependencies and raise an error if found:
    check_dependencies --raise-extra-error extra_deps.txt
"""

import sys
import argparse
from .core import get_list, parse_deps_tree, add_info, print_deps_tree, print_deps_tree_with_info, \
    write_deps_tree_to_file, write_deps_tree_with_info_to_file, find_missing_pkgs, \
    check_and_raise_error


def main():
    """
    Main function for the check_requirements.

    Parses command-line arguments and executes the specified actions based on the arguments.
    """
    parser = argparse.ArgumentParser(description="check_requirements")
    parser.add_argument("--list", "-l", action="store_true", help="List dependencies to console")
    parser.add_argument("--list-file", "-lf", type=str, help="Save dependencies to a file")
    parser.add_argument("--check-missing", "-cm", type=str, help="Check for missing dependencies and print")
    parser.add_argument("--check-extra", "-ce", type=str, help="Check for extra dependencies and print")
    parser.add_argument("--raise-missing-error", "-rme", action="store_true", help="Check for missing dependencies "
                                                                                   "and raise error")
    parser.add_argument("--raise-extra-error", "-ree", action="store_true", help="Check for extra dependencies and "
                                                                                 "raise error")
    parser.add_argument("--ignore", "-i", type=str, help="File containing ignored packages")
    parser.add_argument("--ignore-packages", "-ip", nargs="+", help="List of packages to ignore")
    parser.add_argument("--with-info", "-wi", action="store_true", help="Include Python version and OS info")
    args = parser.parse_args()
    if args.list or args.list_file:
        deps = parse_deps_tree(get_list())
        deps = add_info(deps)
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        sys_platform = sys.platform.lower()
        if args.with_info:
            if args.list:
                print_deps_tree_with_info(deps, python_version, sys_platform)
            if args.list_file:
                write_deps_tree_with_info_to_file(args.list_file, deps, python_version, sys_platform)
        else:
            if args.list:
                print_deps_tree(deps)
            if args.list_file:
                write_deps_tree_to_file(args.list_file, deps)
    ignored_pkgs = []
    if args.check_missing or args.check_extra or args.raise_missing_error or args.raise_extra_error:
        dep_file = [check for check in [args.check_missing, args.check_extra] if check is not None][0]
        dep_lines = None
        if dep_file:
            with open(dep_file, "r", encoding="utf-8") as file:
                dep_lines = file.read()
        if args.ignore:
            with open(args.ignore, 'r', encoding="utf-8") as file:
                ignore_lines = file.read()
                ignored_pkgs = parse_deps_tree(ignore_lines)
        elif args.ignore_packages:
            ignored_pkgs = parse_deps_tree(f"{chr(10).join(args.ignore_packages)}\n")
    if args.check_missing:
        deps_a = parse_deps_tree(get_list())
        deps_b = parse_deps_tree(dep_lines)
        deps_a = add_info(deps_a)
        deps_b = add_info(deps_b)
        missing_pkgs = find_missing_pkgs(deps_a, deps_b, ignored_pkgs)
        for pkg in missing_pkgs:
            print(f"Missing: {pkg['name']}{'==' if pkg.get('version') != '' else ''}{pkg.get('version')}")
    if args.check_extra:
        deps_a = parse_deps_tree(dep_lines)
        deps_b = parse_deps_tree(get_list())
        deps_a = add_info(deps_a)
        deps_b = add_info(deps_b)
        extra_pkgs = find_missing_pkgs(deps_a, deps_b, ignored_pkgs)
        for pkg in extra_pkgs:
            print(f"Extra: {pkg['name']}{'==' if pkg.get('version') != '' else ''}{pkg.get('version')}")
    if args.raise_missing_error and args.check_missing:
        deps_a = parse_deps_tree(get_list())
        deps_b = parse_deps_tree(args.check_missing)
        deps_a = add_info(deps_a)
        deps_b = add_info(deps_b)
        check_and_raise_error(deps_a, deps_b, ignored_pkgs)
    if args.raise_extra_error and args.check_extra:
        deps_a = parse_deps_tree(args.check_extra)
        deps_b = parse_deps_tree(get_list())
        deps_a = add_info(deps_a)
        deps_b = add_info(deps_b)
        check_and_raise_error(deps_a, deps_b, ignored_pkgs)


if __name__ == "__main__":
    main()
