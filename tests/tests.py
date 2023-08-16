"""
This module contains unit tests for the functions and features provided by the check_requirements.

The tests cover various aspects of dependency management, including listing dependencies, checking for missing
or extra packages, ignoring packages, and raising errors for missing or extra dependencies.
"""

import os
import sys
import platform
import re
from contextlib import suppress
from unittest import TestCase
from dummy_package_manager import DummyPackage
from .helpers import _search_pattern, _read_file, _dummy_pkg_file, _pkg_file
from .testers import get_list_tester, parse_deps_tree_tester, add_info_tester, filter_deps_tree_tester, \
    print_deps_tree_tester, write_deps_tree_to_file_tester, is_pkg_in_subtree_tester, find_missing_pkgs_tester, \
    check_and_raise_error_tester, main_tester

PYTHON_VERSION = ".".join(platform.python_version_tuple()[:2])


def test_get_list():
    """
    Test if the get_list function correctly lists dependencies.
    """
    assert _search_pattern(get_list_tester(), r"([^\s]+)==[^\n]+", re.DOTALL)


def test_parse_deps_tree():
    """
    Test if the parse_deps_tree function correctly parses dependency tree structures.
    """
    deps = parse_deps_tree_tester("package1 == 1.0\n  package2 == 2.0\n    package3 == 3.0")
    assert isinstance(deps, list)
    assert len(deps) == 1
    assert deps[0]["name"] == "package1"
    assert len(deps[0]["deps"]) == 1
    assert deps[0]["deps"][0]["name"] == "package2"


def test_add_info():
    """
    Test if the add_info function correctly adds Python version and system platform information to dependencies.
    """
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    deps_with_info = add_info_tester(deps, python_version=PYTHON_VERSION, sys_platform=sys.platform)
    assert isinstance(deps_with_info, list)
    assert deps_with_info[0]["python_version"] == PYTHON_VERSION
    assert deps_with_info[0]["sys_platform"] == sys.platform
    assert deps_with_info[0]["deps"][0]["python_version"] == PYTHON_VERSION
    assert deps_with_info[0]["deps"][0]["sys_platform"] == sys.platform


def test_filter_deps_tree():
    """
    Test the filter_deps_tree function.

    This test function checks the behavior of the filter_deps_tree function by providing a sample dependency tree
    with additional information such as Python version and system platform. It then filters the tree using various
    criteria and asserts the correctness of the filtered results.

    Test cases cover filtering by 'name', 'version', 'python_version', and 'sys_platform'.
    """
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [],
            "python_version": "3.7",
            "sys_platform": "linux"
        },
        {
            "name": "package2",
            "version": "2.0",
            "deps": [],
            "python_version": "3.8",
            "sys_platform": "win32"
        },
        {
            "name": "package3",
            "version": "3.0",
            "deps": [],
            "python_version": "3.9",
            "sys_platform": "linux"
        }
    ]

    # Test filtering by name
    filtered_deps = filter_deps_tree_tester(deps, name="package2")
    assert len(filtered_deps) == 1
    assert filtered_deps[0]["name"] == "package2"

    # Test filtering by version
    filtered_deps = filter_deps_tree_tester(deps, version="1.0")
    assert len(filtered_deps) == 1
    assert filtered_deps[0]["version"] == "1.0"

    # Test filtering by python_version
    filtered_deps = filter_deps_tree_tester(deps, python_version="3.8")
    assert len(filtered_deps) == 1
    assert filtered_deps[0]["python_version"] == "3.8"

    # Test filtering by sys_platform
    filtered_deps = filter_deps_tree_tester(deps, sys_platform="linux")
    assert len(filtered_deps) == 2
    assert all(pkg["sys_platform"] == "linux" for pkg in filtered_deps)

    # Test filtering by name, version, python_version, and sys_platform
    filtered_deps = filter_deps_tree_tester(
        deps,
        name="package3",
        version="3.0",
        python_version="3.9",
        sys_platform="linux"
    )
    assert len(filtered_deps) == 1
    assert filtered_deps[0]["name"] == "package3"
    assert filtered_deps[0]["version"] == "3.0"
    assert filtered_deps[0]["python_version"] == "3.9"
    assert filtered_deps[0]["sys_platform"] == "linux"

    # Test filtering with no matches
    filtered_deps = filter_deps_tree_tester(deps, name="nonexistent_package")
    assert len(filtered_deps) == 0


def test_print_deps_tree():
    """
    Test if the print_deps_tree function correctly prints the dependency tree structure.
    """
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    printed_lines = print_deps_tree_tester(deps)
    assert printed_lines[0] == "package1 == 1.0"
    assert printed_lines[1] == "  package2 == 2.0"
    assert len(printed_lines) == 3
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    deps = add_info_tester(deps, python_version=PYTHON_VERSION, sys_platform=sys.platform)
    assert deps[0]["python_version"] == PYTHON_VERSION
    assert deps[0]["sys_platform"] == sys.platform
    assert deps[0]["deps"][0]["python_version"] == PYTHON_VERSION
    assert deps[0]["deps"][0]["sys_platform"] == sys.platform
    printed_lines = print_deps_tree_tester(deps)
    assert printed_lines[0] == f"package1 == 1.0; "\
                               f"python_version == {PYTHON_VERSION} and "\
                               f"sys_platform == {sys.platform}"
    assert printed_lines[1] == f"  package2 == 2.0; "\
                               f"python_version == {PYTHON_VERSION} and "\
                               f"sys_platform == {sys.platform}"
    assert len(printed_lines) == 3


def test_write_deps_tree_to_file():
    """
    Test if the write_deps_tree_to_file function correctly writes the dependency tree to a file.
    """
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]

    written_lines = write_deps_tree_to_file_tester(deps)
    expected_lines = [
        "package1 == 1.0\n",
        "  package2 == 2.0\n"
    ]
    assert written_lines == expected_lines
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    deps = add_info_tester(deps, python_version=PYTHON_VERSION, sys_platform=sys.platform)
    assert deps[0]["python_version"] == PYTHON_VERSION
    assert deps[0]["sys_platform"] == sys.platform
    assert deps[0]["deps"][0]["python_version"] == PYTHON_VERSION
    assert deps[0]["deps"][0]["sys_platform"] == sys.platform
    written_lines = write_deps_tree_to_file_tester(deps)
    expected_lines = [
        f"package1 == 1.0; python_version == {PYTHON_VERSION}"
        f" and sys_platform == {sys.platform}\n",
        f"  package2 == 2.0; python_version == {PYTHON_VERSION}"
        f" and sys_platform == {sys.platform}\n"
    ]
    assert written_lines == expected_lines


def test_is_pkg_in_subtree():
    """
    Test if the is_pkg_in_subtree function correctly checks if a package is present in a dependency subtree.
    """
    pkg = {
        "name": "package2",
        "version": "2.0"
    }
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    assert is_pkg_in_subtree_tester(pkg, deps)
    pkg = {
        "name": "package2",
        "version": "2.0"
    }
    deps = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": []
        }
    ]
    assert not is_pkg_in_subtree_tester(pkg, deps)


def test_find_missing_pkgs():
    """
    Test if the find_missing_pkgs function correctly identifies missing packages between two dependency trees.
    """
    deps_a = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    deps_b = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": []
        }
    ]
    ignored_pkgs = []
    missing_pkgs = find_missing_pkgs_tester(deps_a, deps_b, ignored_pkgs)
    assert isinstance(missing_pkgs, list)
    assert len(missing_pkgs) == 1
    assert missing_pkgs == [{"name": "package2", "version": "2.0", "deps": []}]
    assert missing_pkgs[0]["name"] == "package2"
    assert missing_pkgs[0]["version"] == "2.0"


def test_find_missing_pkgs__ignored():
    """
    Test if the find_missing_pkgs function correctly identifies missing packages
    considering the ignored packages.
    """
    deps_a = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        },
        {
            "name": "ignored_package_1",
            "version": "1.0",
            "deps": []
        },
        {
            "name": "ignored_package_2",
            "version": "2.0.0",
            "deps": []
        }
    ]
    deps_b = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": []
        }
    ]
    ignored_pkgs = [
        {"name": "ignored_package_1", "version": "", "deps": []},
        {"name": "ignored_package_2", "version": "2.0.0", "deps": []}
    ]
    missing_pkgs = find_missing_pkgs_tester(deps_a, deps_b, ignored_pkgs)
    assert isinstance(missing_pkgs, list)
    assert len(missing_pkgs) == 1
    assert missing_pkgs[0]["name"] == "package2"
    assert missing_pkgs[0]["version"] == "2.0"


def test_check_and_raise_error():
    """
    Test if the check_and_raise_error function correctly checks and raises errors for missing or extra dependencies.
    """
    deps_a = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        }
    ]
    deps_b = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": []
        }
    ]
    ignored_pkgs = []
    check_and_raise_error_tester(deps_a, deps_b, ignored_pkgs)


def test_check_and_raise_error__ignored():
    """
    Test if the check_and_raise_error function correctly checks and raises errors with ignored packages.
    """
    deps_a = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": [
                {
                    "name": "package2",
                    "version": "2.0",
                    "deps": []
                }
            ]
        },
        {
            "name": "ignored_package_1",
            "version": "1.0",
            "deps": []
        },
        {
            "name": "ignored_package_2",
            "version": "2.0.0",
            "deps": []
        }
    ]
    deps_b = [
        {
            "name": "package1",
            "version": "1.0",
            "deps": []
        }
    ]
    ignored_pkgs = [
        {"name": "ignored_package_1", "version": "", "deps": []},
        {"name": "ignored_package_2", "version": "2.0.0", "deps": []}
    ]
    check_and_raise_error_tester(deps_a, deps_b, ignored_pkgs)


def test_main__help():
    """
    Test the command-line help output for the main script.
    """
    expected_output = "usage: check_requirements [-h] [--list] [--list-file LIST_FILE]\n                          " \
                      "[--check-missing CHECK_MISSING]\n                          [--check-extra CHECK_EXTRA] [" \
                      "--raise-missing-error]\n                          [--raise-extra-error] [--ignore IGNORE]\n   " \
                      "                       [--ignore-packages IGNORE_PACKAGES [IGNORE_PACKAGES ...]]\n            " \
                      "              [--with-info]\n\ncheck_requirements\n\noptional arguments:\n  -h, --help        " \
                      "    show this help message and exit\n  --list, -l            List dependencies to console\n  " \
                      "--list-file LIST_FILE, -lf LIST_FILE\n                        Save dependencies to a file\n  " \
                      "--check-missing CHECK_MISSING, -cm CHECK_MISSING\n                        Check for missing " \
                      "dependencies and print\n  --check-extra CHECK_EXTRA, -ce CHECK_EXTRA\n                        " \
                      "Check for extra dependencies and print\n  --raise-missing-error, -rme\n                       " \
                      "Check for missing dependencies and raise error\n  --raise-extra-error, -ree\n                 " \
                      "        Check for extra dependencies and raise error\n  --ignore IGNORE, -i IGNORE\n          " \
                      "              File containing ignored packages\n  --ignore-packages IGNORE_PACKAGES [" \
                      "IGNORE_PACKAGES ...], -ip IGNORE_PACKAGES [IGNORE_PACKAGES ...]\n                        List " \
                      "of packages to ignore\n  --with-info, -wi      Include requested system information\n"
    with suppress(SystemExit):
        assert expected_output == main_tester("check_requirements -h")


def test_main__list():
    """
    Test listing dependencies to the console using the main script.
    """
    assert _search_pattern(main_tester("check_requirements -l"), r"([^\s]+) == [^\n]+", re.DOTALL)


def test_main__list_with_info():
    """
    Test listing dependencies with additional information to the console using the main script.
    """
    assert _search_pattern(
        main_tester("check_requirements -l -wi sys_platform python_version"),
        r"([\w-]+) == [\d.]+; sys_platform == \w+ and python_version == \d\.\d{1,2}",
        0
    )


def test_main__list_file():
    """
    Test saving dependencies to a file using the main script.
    """
    main_tester("check_requirements -lf output.txt")
    assert _search_pattern(_read_file("output.txt"), r"([^\s]+) == [^\n]+", re.DOTALL)
    os.remove("output.txt")


def test_main__list_file_with_info():
    """
    Test saving dependencies with additional information to a file using the main script.
    """
    main_tester("check_requirements -lf output.txt -wi sys_platform python_version")
    assert _search_pattern(
        _read_file("output.txt"),
        r"([\w-]+) == [\d.]+; sys_platform == \w+ and python_version == \d\.\d{1,2}",
        0
    )
    os.remove("output.txt")


def test_main__check_missing():
    """
    Test checking for missing dependencies using the main script.
    """
    with DummyPackage("package1") as dummy_pkg:
        dummy_pkg.install()
        assert "package1" in main_tester("check_requirements -cm requirements.txt")


def test_main__check_missing_ignore():
    """
    Test checking for missing dependencies using the main script while ignoring specified packages.
    """
    with DummyPackage("package1", requirements=["package2"]) as dummy_pkg:
        dummy_pkg.install()
        is_installed = dummy_pkg.package["is_installed"]
        while not is_installed:
            is_installed = dummy_pkg.package["is_installed"]
        with _pkg_file(["package1 == 0.1.0"]) as ignored:
            output = main_tester(f"check_requirements -cm requirements.txt -i {ignored.file.name}")
            assert "package1 == 0.1.0" not in output
            assert "package2 == 0.1.0" in output


def test_main__check_missing_ignore_packages():
    """
    Test checking for missing dependencies using the main script while ignoring specified packages.
    """
    with DummyPackage("package1", requirements=["package2"]) as dummy_pkg:
        dummy_pkg.install()
        output = main_tester("check_requirements -cm requirements.txt -ip package1==0.1.0")
        assert "package1 == 0.1.0" not in output
        assert "package2 == 0.1.0" in output


def test_main__check_missing_ignore__2():
    """
    Test checking for missing dependencies using the main script while ignoring specified packages.
    """
    with DummyPackage("package1") as dummy_pkg_1:
        with DummyPackage("package2") as dummy_pkg_2:
            dummy_pkg_1.install()
            dummy_pkg_2.install()
            with _pkg_file(["package1 == 0.1.0"]) as ignored:
                output = main_tester(f"check_requirements -cm requirements.txt -i {ignored.file.name}")
                assert "package1 == 0.1.0" not in output
                assert "package2 == 0.1.0" in output


def test_main__check_missing_ignore_packages__2():
    """
    Test checking for missing dependencies using the main script while ignoring specified packages.
    """
    with DummyPackage("package1") as dummy_pkg_1:
        with DummyPackage("package2") as dummy_pkg_2:
            dummy_pkg_1.install()
            dummy_pkg_2.install()
            output = main_tester("check_requirements -cm requirements.txt -ip package1==0.1.0")
            assert "package1 == 0.1.0" not in output
            assert "package2 == 0.1.0" in output


def test_main__check_extra():
    """
    Test checking for extra dependencies using the main script.
    """
    with _dummy_pkg_file(1) as dummy:
        output = main_tester(f"check_requirements -ce {dummy.file.name}")
        assert "package1" in output


def test_main__check_extra_ignore():
    """
    Test checking for extra dependencies using the main script while ignoring specified packages.
    """
    with _dummy_pkg_file(1) as dummy_to_ignore:
        with _dummy_pkg_file(2) as dummy_to_extra:
            output = main_tester(f"check_requirements -ce {dummy_to_extra.file.name} -i {dummy_to_ignore.file.name}")
            assert "package1" not in output
            assert "package2" in output


def test_main__check_extra_ignore_packages():
    """
    Test if the main function correctly raises ImportError for missing dependencies while ignoring specified packages.
    """
    with _dummy_pkg_file(2) as dummy_to_extra:
        output = main_tester(f"check_requirements -ce {dummy_to_extra.file.name} -ip package1")
        assert "package1" not in output
        assert "package2" in output


def test_main__raise_missing_error():
    """
    Test if the main function correctly raises ImportError for missing dependencies without ignoring any packages.
    """
    with DummyPackage("package1") as dummy_pkg:
        dummy_pkg.install()
        with TestCase().assertRaises(ImportError):
            assert "package1" in main_tester("check_requirements -cm requirements.txt -rme")


def test_main__raise_missing_error_ignore():
    """
    Test if the main function correctly raises ImportError for missing dependencies while ignoring specified packages.
    """
    with DummyPackage("package1", requirements=["package2"]) as dummy_pkg:
        dummy_pkg.install()
        with _pkg_file(["package1 == 0.1.0"]) as ignored:
            with TestCase().assertRaises(ImportError):
                output = main_tester(f"check_requirements -cm requirements.txt -i {ignored.file.name} -rme")
                assert "package1 == 0.1.0" not in output
                assert "package2 == 0.1.0" in output


def test_main__raise_missing_error_ignore_packages():
    """
    Test if the main function correctly raises ImportError for missing dependencies while ignoring specified packages.
    """
    with DummyPackage("package1", requirements=["package2"]) as dummy_pkg:
        dummy_pkg.install()
        with TestCase().assertRaises(ImportError):
            output = main_tester("check_requirements -cm requirements.txt -ip package1==0.1.0 -rme")
            assert "package1 == 0.1.0" not in output
            assert "package2 == 0.1.0" in output


def test_main__raise_extra_error():
    """
    Test if the main function correctly raises ImportError for extra dependencies.
    """
    case = TestCase()
    with _dummy_pkg_file(1) as dummy:
        with case.assertRaises(ImportError):
            assert "package1" in main_tester(f"check_requirements -ce {dummy.file.name} -ree")


def test_main__raise_extra_error_ignore():
    """
    Test if the main function correctly raises ImportError for extra dependencies while ignoring specified packages.
    """
    case = TestCase()
    with _dummy_pkg_file(1) as dummy_to_ignore:
        with _dummy_pkg_file(2) as dummy_to_extra:
            with case.assertRaises(ImportError):
                output = main_tester(
                    f"check_requirements -ce {dummy_to_extra.file.name} -i {dummy_to_ignore.file.name} -ree"
                )
                assert "package1" not in output
                assert "package2" in output


def test_main__raise_extra_error_ignore_packages():
    """
    Test if the main function correctly raises ImportError for extra dependencies while ignoring specified
    packages.
    """
    case = TestCase()
    with _dummy_pkg_file(2) as dummy_to_extra:
        with case.assertRaises(ImportError):
            output = main_tester(f"check_requirements -ce {dummy_to_extra.file.name} -ip package1 -ree")
            assert "package1" not in output
            assert "package2" in output
