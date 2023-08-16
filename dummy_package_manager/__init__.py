"""
dummy_package_manager

Effortlessly create and manage dummy Python packages.

The dummy_package_manager module offers a streamlined approach to generating
and handling dummy Python packages along with their optional dependencies.
This tool is designed to simplify testing, experimentation, and development
tasks that involve temporary package setups.

Example usage:
    from dummy_package_manager import DummyPackage

    with DummyPackage("mypackage", ["dependency1", "dependency2"]) as dummy_pkg:
        print(f"{dummy_pkg.package['name']} package created at {dummy_pkg.package['source_dir']}")
        # Perform testing or experimentation

Key Features:
    - Create temporary dummy packages with optional dependencies.
    - Simplify the process of setting up isolated testing environments.
    - Easily manage package installations and uninstallations.
    - Designed for use in testing, experimentation, and development workflows.
"""

from __future__ import absolute_import

# meta
__title__ = "dummy_package_manager"
__author__ = "Eftal Gezer"
__license__ = "GNU GPL v3"
__copyright__ = "Copyright 2023, Eftal Gezer"
__version__ = "0.1.0"

from .core import DummyPackage
