"""
This script is used to run the unit tests for the `check_requirements` package.

It imports all the defined unit test functions from the `tests` module and executes them. The script is intended
to be run as the main entry point for running the unit tests.

Usage:
    python -m check_requirements.tests.__main__

Note:
    The unit test functions are responsible for checking various aspects of the `check_requirements` package,
    including listing dependencies, parsing dependency tree structures, checking for missing or extra packages,
    ignoring packages, and raising errors for missing or extra dependencies.
"""

from .tests import (test_get_list,
                    test_parse_deps_tree,
                    test_add_info,
                    test_print_deps_tree,
                    test_print_deps_tree_with_info,
                    test_write_deps_tree_to_file,
                    test_write_deps_tree_with_info_to_file,
                    test_is_pkg_in_subtree,
                    test_find_missing_pkgs,
                    test_find_missing_pkgs__ignored,
                    test_check_and_raise_error,
                    test_check_and_raise_error__ignored,
                    test_main__help,
                    test_main__list,
                    test_main__list_with_info,
                    test_main__list_file,
                    test_main__list_file_with_info,
                    test_main__check_missing,
                    test_main__check_missing_ignore,
                    test_main__check_missing_ignore_packages,
                    test_main__check_extra,
                    test_main__check_extra_ignore,
                    test_main__check_extra_ignore_packages,
                    test_main__raise_missing_error,
                    test_main__raise_missing_error_ignore,
                    test_main__raise_missing_error_ignore_packages,
                    test_main__raise_extra_error,
                    test_main__raise_extra_error_ignore,
                    test_main__raise_extra_error_ignore_packages
                    )
if __name__ == "__main__":
    test_get_list()
    test_parse_deps_tree()
    test_add_info()
    test_print_deps_tree()
    test_print_deps_tree_with_info()
    test_write_deps_tree_to_file()
    test_write_deps_tree_with_info_to_file()
    test_is_pkg_in_subtree()
    test_find_missing_pkgs()
    test_find_missing_pkgs__ignored()
    test_check_and_raise_error()
    test_check_and_raise_error__ignored()
    test_main__help()
    test_main__list()
    test_main__list_with_info()
    test_main__list_file()
    test_main__list_file_with_info()
    test_main__check_missing()
    test_main__check_missing_ignore()
    test_main__check_missing_ignore_packages()
    test_main__check_extra()
    test_main__check_extra_ignore()
    test_main__check_extra_ignore_packages()
    test_main__raise_missing_error()
    test_main__raise_missing_error_ignore()
    test_main__raise_missing_error_ignore_packages()
    test_main__raise_extra_error()
    test_main__raise_extra_error_ignore()
    test_main__raise_extra_error_ignore_packages()
