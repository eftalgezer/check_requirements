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
import os
import sys
import platform
import argparse
from .core import get_list, parse_deps_tree, add_info, ignore_pkgs, format_full_version
from .cli import list_deps, list_file, check_missing, check_extra, raise_missing_error, raise_extra_error, \
    process_deps_file


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
    parser.add_argument("--with-info", "-wi", nargs="+", help="Include requested system information")
    args = parser.parse_args()
    sys_info = {
        "os_name": os.name,
        "sys_platform": sys.platform,
        "platform_machine": platform.machine(),
        "platform_python_implementation": platform.python_implementation(),
        "platform_release": platform.release(),
        "platform_system": platform.system(),
        "platform_version": platform.version(),
        "python_version": ".".join(platform.python_version_tuple()[:2]),
        "python_full_version": platform.python_version(),
        "implementation_name": sys.implementation.name,
        "implementation_version": format_full_version()
    }
    deps = parse_deps_tree(get_list())
    file_deps = None
    ignored_pkgs = None
    if args.with_info and (args.list or args.list_file):
        sys_info_req = {key: sys_info[key] for key in args.with_info}
        deps = add_info(deps, **sys_info_req)
    if args.ignore:
        with open(args.ignore, 'r', encoding="utf-8") as file:
            ignore_lines = file.read()
            ignored_pkgs = parse_deps_tree(ignore_lines)
            if not args.check_extra:
                deps = ignore_pkgs(deps, ignored_pkgs)
    elif args.ignore_packages:
        ignored_pkgs = parse_deps_tree(f"{chr(10).join(args.ignore_packages)}\n")
        if not args.check_extra:
            deps = ignore_pkgs(deps, ignored_pkgs)
    if args.check_missing or args.check_extra:
        dep_file = [check for check in [args.check_missing, args.check_extra] if check][0]
        if dep_file:
            file_deps = process_deps_file(dep_file, sys_info)
            if args.check_extra and file_deps:
                file_deps = ignore_pkgs(file_deps, ignored_pkgs)
    if args.list:
        list_deps(deps)
    if args.list_file:
        list_file(deps, args.list_file)
    if args.check_missing:
        check_missing(deps, file_deps)
    if args.check_extra:
        check_extra(deps, file_deps)
    if args.raise_missing_error and args.check_missing:
        raise_missing_error(deps, file_deps)
    if args.raise_extra_error and args.check_extra:
        raise_extra_error(deps, file_deps)


if __name__ == "__main__":
    main()
