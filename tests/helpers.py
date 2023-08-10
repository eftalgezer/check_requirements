"""
This module contains utility functions and classes used for testing purposes in the check_requirements package.

The functions and classes defined in this module help simulate specific scenarios, capture standard output, and
provide temporary files for testing the functionalities of the check_requirements package.
"""

import os
import sys
from io import StringIO
from tempfile import NamedTemporaryFile
from subprocess import Popen
from shlex import split
import re


def _capture_stdout(func, *args, **kwargs):
    """
    Capture and return the standard output produced by a function.

    Args:
        func: The function whose standard output needs to be captured.
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Returns:
        str: Captured standard output as a string.
    """
    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout
    try:
        func(*args, **kwargs)
        sys.stdout.seek(0)
        return new_stdout.read()
    finally:
        sys.stdout = old_stdout


def _search_pattern(text, pattern, flag):
    """
    Search for a regular expression pattern in a given text.

    Args:
        text (str): The text to search within.
        pattern (str): The regular expression pattern to search for.
        flag: Flags to control regular expression matching.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    pattern = re.compile(pattern, flag)
    match = pattern.search(text)
    if match:
        return True
    return False


def _read_file(file_path):
    """
    Read the contents of a file.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


class _pkg:
    """
    Context manager class to install and uninstall a Python package for testing purposes.

    This class is designed to be used as a context manager to install and uninstall a specified Python package
    using the pip command line utility.

    Args:
        package (str): The name of the Python package to be installed and uninstalled.

    Usage:
        with _pkg("package_name"):
            # The specified package is installed within this context
            # Do your tests here
        # The package is uninstalled automatically when exiting the context

    Attributes:
        package (str): The name of the Python package.

    Methods:
        __enter__(): Install the specified package when entering the context.
        __exit__(): Uninstall the specified package when exiting the context.
    """

    def __init__(self, package):
        """
        Initialize the _pkg object with the specified package name.
        """
        self.package = package

    def __enter__(self):
        """
        Install the specified package when entering the context.
        """
        Popen(split(f"python -m pip install {self.package} --no-input"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Popen(split(f"python -m pip uninstall {self.package} --yes"))


class _dummy_pkg_file:
    """
    Context manager class to create a temporary file with dummy package names for testing purposes.

    This class is designed to be used as a context manager to create a temporary file with a specified number of
    dummy package names and versions. The created file can be used as a mock requirements.txt file for testing.

    Args:
        count (int): The number of dummy package names to generate.

    Usage:
        with _dummy_pkg_file(3) as dummy:
            # A temporary file is created with dummy package names
            # Do your tests here
        # The temporary file is automatically deleted when exiting the context

    Attributes:
        count (int): The number of dummy package names to generate.
        file (file-like object): The temporary file object.

    Methods:
        __enter__(): Create the temporary file and write dummy package names.
        __exit__(): Delete the temporary file when exiting the context.
    """

    def __init__(self, count):
        """
        Initialize the _dummy_pkg_file object with the specified count.
        """
        self.count = count
        self.file = NamedTemporaryFile(delete=False)

    def __enter__(self):
        """
        Create the temporary file and write dummy package names.
        """
        with self.file:
            for i in range(1, self.count):
                self.file.write(f"package{i}==0.1.0\n".encode("utf-8"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Delete the temporary file when exiting the context.
        """
        os.remove(self.file.name)


class _pkg_file:
    """
    Context manager class to create a temporary file with specified package names for testing purposes.

    This class is designed to be used as a context manager to create a temporary file with a list of specified
    package names and versions. The created file can be used as a mock requirements.txt file for testing.

    Args:
        pkgs (list): A list of strings representing package names and versions.

    Usage:
        with _pkg_file(["package1==0.1.0", "package2==1.0.0"]) as pkg_file:
            # A temporary file is created with specified package names
            # Do your tests here
        # The temporary file is automatically deleted when exiting the context

    Attributes:
        pkgs (list): A list of strings representing package names and versions.
        file (file-like object): The temporary file object.

    Methods:
        __enter__(): Create the temporary file and write specified package names.
        __exit__(): Delete the temporary file when exiting the context.
    """

    def __init__(self, pkgs):
        """
        Initialize the _pkg_file object with the specified package list.
        """
        self.pkgs = pkgs
        self.file = NamedTemporaryFile(delete=False)

    def __enter__(self):
        """
        Create the temporary file and write specified package names.
        """
        with self.file:
            for pkg in self.pkgs:
                pkg = f"{pkg}\n"
                self.file.write(pkg.encode("utf-8"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Delete the temporary file when exiting the context.
        """
        os.remove(self.file.name)
