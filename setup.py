"""
Setup file for check_requirements
"""
from __future__ import absolute_import
import os
from setuptools import setup

HERE = os.getcwd().replace("{0}setup.py".format(os.sep), "")

LONG_DESCRIPTION = ""

with open("{0}{1}README.md".format(HERE, os.sep), "r", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name="check_requirements",
    version="0.1.0",
    description="Dependency management tools for Python packages.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/eftalgezer/check_requirements",
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
    keywords="dependency management, python packages, dependency checking, requirements, dependency tree, dependency "
             "analysis",
    packages=["check_requirements"],
    zip_safe=False,
    include_package_data=True,
    install_requires=["pipdeptree"],
    project_urls={
        "Bug Reports": "https://github.com/eftalgezer/check_requirements/issues",
        "Source": "https://github.com/eftalgezer/check_requirements",
        "Blog": "https://beyondthearistotelian.blogspot.com/search/label/check_requirements",
        "Developer": "https://www.eftalgezer.com/",
    },
    entry_points={
        "console_scripts": [
            "check_requirements=check_requirements.__main__:main",
        ]
    },
)
