# Address parser

[![pypi](https://img.shields.io/pypi/v/addrparser.svg)](https://pypi.org/project/addrparser/)
[![python](https://img.shields.io/pypi/pyversions/addrparser.svg)](https://pypi.org/project/addrparser/)
[![Build Status](https://github.com/gispocoding/addr-parser/actions/workflows/dev.yml/badge.svg)](https://github.com/gispocoding/addr-parser/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/gispocoding/addr-parser/branch/main/graphs/badge.svg)](https://codecov.io/github/gispocoding/addr-parser)

Simple address parser with localization support.

> **Note:**
> This library is meant to be simple, light weight and easy to adapt. This is not the best and most optimized address parser out there.
> For *state of the art* parser you should probably look at https://github.com/openvenues/pypostal

* Documentation: <https://gispocoding.github.io/addr-parser>
* GitHub: <https://github.com/gispocoding/addr-parser>
* PyPI: <https://pypi.org/project/addrparser/>
* Free software: MIT

## Supported countries
| Country         | Description                            | Documentation                                          |
| --------------- | -------------------------------------- | ------------------------------------------------------ |
| Suomi - Finland | Suomalaisten osoitteiden osoiteparseri | <https://gispocoding.github.io/addr-parser/locales/fi> |

## Installation

```
pip install addrparser
```

### Setting up a development environment
See instructions in [CONTRIBUTING.md](./CONTRIBUTING.md#get-started)

## Usage

### Command line tool
```shell
$ addr-parse --help
Usage: addr-parse [OPTIONS] ADDRESS

  Cli tool for parsing text addresses.

  Args:     address (str): address text

Options:
  -l, --locale TEXT  Country code in two-letter ISO 3166
  --help             Show this message and exit.
```

```shell
$ addr-parser "Iso Maantie 12b B 7"
{
  "input": "Iso Maantie 12b B 7",
  "result": {
    "street_name": "Iso Maantie",
    "house_number": "12b",
    "entrance": "B",
    "apartment": "7"
  }
}
```
### Library
```python
>>> from addrparser import AddressParser

>>> parser = AddressParser('fi')
>>> address = parser.parse('Iso Maantie 12b B 7')
>>> address
Address(street_name='Iso Maantie', house_number='12b', entrance='B', apartment='7', post_office_box=None, zip_number=None, zip_name=None)
```

## Credits

This project was created with inspiration from [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
