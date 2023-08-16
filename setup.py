"""
Setup file for dummy_package_manager
"""
from __future__ import absolute_import
import os
from setuptools import setup

HERE = os.getcwd().replace("{0}setup.py".format(os.sep), "")

LONG_DESCRIPTION = ""

with open("{0}{1}README.md".format(HERE, os.sep), "r", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name="dummy_package_manager",
    version="0.1.0",
    description="A utility for creating and managing dummy Python packages with optional dependencies.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/eftalgezer/dummy_package_manager",
    author="Eftal Gezer",
    author_email="eftal.gezer@astrobiyoloji.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education :: Testing",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities"
    ],
    keywords="dummy package, dummy, package, utility, dependencies, testing",
    packages=["dummy_package_manager"],
    zip_safe=False,
    include_package_data=True,
    install_requires=["pip"],
    project_urls={
        "Bug Reports": "https://github.com/eftalgezer/dummy_package_manager/issues",
        "Source": "https://github.com/eftalgezer/dummy_package_manager",
        "Blog": "https://beyondthearistotelian.blogspot.com/search/label/dummy_package_manager",
        "Developer": "https://www.eftalgezer.com/",
    },
)
