# check_requirements
[![PyPI version](https://badge.fury.io/py/check_requirements.svg)](https://badge.fury.io/py/check_requirements)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/check_requirements.svg)](https://pypi.python.org/pypi/check_requirements/)
[![Python package](https://github.com/eftalgezer/check_requirements/actions/workflows/python-package.yml/badge.svg)](https://github.com/eftalgezer/check_requirements/actions/workflows/python-package.yml)
[![Check requirements](https://github.com/eftalgezer/check_requirements/actions/workflows/check-requirements.yml/badge.svg)](https://github.com/eftalgezer/check_requirements/actions/workflows/check-requirements.yml)
[![codecov](https://codecov.io/gh/eftalgezer/check_requirements/branch/main/graph/badge.svg?token=Q9TJFIN1U1)](https://codecov.io/gh/eftalgezer/check_requirements)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f0c0e8e9cf6a4151ac39bbad05e3c535)](https://app.codacy.com/gh/eftalgezer/check_requirements/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![PyPI download month](https://img.shields.io/pypi/dm/check_requirements.svg)](https://pypi.python.org/pypi/check_requirements/)
[![PyPI download week](https://img.shields.io/pypi/dw/check_requirements.svg)](https://pypi.python.org/pypi/check_requirements/)
[![PyPI download day](https://img.shields.io/pypi/dd/check_requirements.svg)](https://pypi.python.org/pypi/check_requirements/)
![GitHub all releases](https://img.shields.io/github/downloads/eftalgezer/check_requirements/total?style=flat)
[![GitHub contributors](https://img.shields.io/github/contributors/eftalgezer/check_requirements.svg)](https://github.com/eftalgezer/check_requirements/graphs/contributors/)
[![CodeFactor](https://www.codefactor.io/repository/github/eftalgezer/check_requirements/badge)](https://www.codefactor.io/repository/github/eftalgezer/check_requirements)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f0c0e8e9cf6a4151ac39bbad05e3c535)](https://app.codacy.com/gh/eftalgezer/check_requirements/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)[![PyPI license](https://img.shields.io/pypi/l/check_requirements.svg)](https://pypi.python.org/pypi/check_requirements/)

check_requirements is a Python tool for managing and analyzing dependencies in your projects. It helps you identify missing and extra dependencies in your project, ensuring a clean and reliable environment. Its error-raising feature is particularly valuable for continuous integration (CI) pipelines, where maintaining a consistent dependency set is crucial.

## Features

- List project dependencies.
- Check for missing and extra dependencies.
- Ignore specific packages.
- Include Python version and system platform information.
- **Raise errors for missing or extra dependencies**, enhancing your CI workflows and preventing unexpected issues in production.

## Installation

check_requirements can be installed using pip:

```bash
pip install check_requirements

# to make sure you have the latest version
pip install -U check_requirements

# latest available code base
pip install -U git+https://github.com/eftalgezer/check_requirements.git
```
## Usage
### Listing Dependencies

To list project dependencies to the console:

```bash

check_requirements -l
```
### Checking for Missing and Extra Dependencies

The primary strength of check_requirements lies in checking for missing and extra dependencies. This is particularly useful for maintaining a consistent environment across different stages of your project.

```bash
# Check for missing dependencies and raise an error if any are found
check_requirements -cm requirements.txt -rme

# Check for extra dependencies and raise an error if any are found
check_requirements -ce requirements.txt -ree
```
Utilizing these checks in your CI pipelines can help catch potential problems before they reach production.

For more information and usage options, refer to the [documentation](https://github.com/eftalgezer/check_requirements/blob/master/docs) .
### Using check_requirements in Python Code

check_requirements can also be utilized directly in your Python code to programmatically manage dependencies and raise errors:

```python
from check_requirements import check_and_raise_error

# Define your project's dependencies
project_deps = [
    # ...
]

# Load existing dependencies from a file or other source
existing_deps = load_existing_dependencies()

# Check for missing dependencies and raise an error if any are found
check_and_raise_error(project_deps, existing_deps)
```
## Unit Tests

check_requirements comes with a comprehensive set of unit tests to ensure its functionality. To run the tests, navigate to the main directory and execute:

```bash
pytest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://github.com/eftalgezer/check_requirements/blob/master/LICENSE) 
