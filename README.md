# dummy_package_manager
[![PyPI version](https://badge.fury.io/py/dummy_package_manager.svg)](https://badge.fury.io/py/dummy_package_manager)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/dummy_package_manager.svg)](https://pypi.python.org/pypi/dummy_package_manager/)
[![Python package](https://github.com/eftalgezer/dummy_package_manager/actions/workflows/python-package.yml/badge.svg)](https://github.com/eftalgezer/dummy_package_manager/actions/workflows/python-package.yml)
[![Check requirements](https://github.com/eftalgezer/dummy_package_manager/actions/workflows/check_requirements/yml/badge.svg)](https://github.com/eftalgezer/dummy_package_manager/actions/workflows/check_requirements.yml)
[![codecov](https://codecov.io/gh/eftalgezer/dummy_package_manager/branch/main/graph/badge.svg?token=Q9TJFIN1U1)](https://codecov.io/gh/eftalgezer/dummy_package_manager)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f0c0e8e9cf6a4151ac39bbad05e3c535)](https://app.codacy.com/gh/eftalgezer/dummy_package_manager/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![PyPI download month](https://img.shields.io/pypi/dm/dummy_package_manager.svg)](https://pypi.python.org/pypi/dummy_package_manager/)
[![PyPI download week](https://img.shields.io/pypi/dw/dummy_package_manager.svg)](https://pypi.python.org/pypi/dummy_package_manager/)
[![PyPI download day](https://img.shields.io/pypi/dd/dummy_package_manager.svg)](https://pypi.python.org/pypi/dummy_package_manager/)
![GitHub all releases](https://img.shields.io/github/downloads/eftalgezer/dummy_package_manager/total?style=flat)
[![GitHub contributors](https://img.shields.io/github/contributors/eftalgezer/dummy_package_manager.svg)](https://github.com/eftalgezer/dummy_package_manager/graphs/contributors/)
[![CodeFactor](https://www.codefactor.io/repository/github/eftalgezer/dummy_package_manager/badge)](https://www.codefactor.io/repository/github/eftalgezer/dummy_package_manager)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/36a170ba82d644bd936095d60b097572)](https://app.codacy.com/gh/eftalgezer/dummy_package_manager/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Effortlessly create and manage dummy Python packages.

The dummy_package_manager module offers a streamlined approach to generating
and handling dummy Python packages along with their optional dependencies.
This tool is designed to simplify testing, experimentation, and development
tasks that involve temporary package setups.

Key Features:
- Create temporary dummy packages with optional dependencies.
- Simplify the process of setting up isolated testing environments.
- Easily manage package installations and uninstallations.
- Designed for use in testing, experimentation, and development workflows.

## Installation

dummy_package_manager can be installed using pip:

```bash
pip install dummy_package_manager

# to make sure you have the latest version
pip install -U dummy_package_manager

# latest available code base
pip install -U git+https://github.com/eftalgezer/dummy_package_manager.git
```

## Usage

You can use the `DummyPackage` class as a context manager to create and manage dummy packages. Here's an example:

```python
from dummy_package_manager import DummyPackage

with DummyPackage("my_package", requirements=["dependency1", "dependency2"]) as dummy_pkg:
    dummy_pkg.install()
    # Your code using the dummy package
    dummy_pkg.uninstall()
```

## Unit Tests

dummy_package_manager comes with a comprehensive set of unit tests to ensure its functionality. To run the tests, navigate to the main directory and execute:

```bash
pytest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://github.com/eftalgezer/dummy_package_manager/blob/master/LICENSE) 