"""
check_requirements: A utility package for managing and checking Python package dependencies.

This package provides tools for listing, comparing, and checking package dependencies in a Python environment.
"""


from __future__ import absolute_import

# meta
__title__ = "check_requirements"
__author__ = "Eftal Gezer"
__license__ = "GNU GPL v3"
__copyright__ = "Copyright 2023, Eftal Gezer"
__version__ = "0.1.0"


from .core import get_list, parse_deps_tree, add_info, filter_deps_tree, print_deps_tree, write_deps_tree_to_file, \
    is_pkg_in_subtree, find_missing_pkgs, check_and_raise_error, format_full_version
