
# WarMAC Beta Version 0.0.2

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Eutropios/WarMAC/main)]((https://github.com/Eutropios/WarMAC))
[![MIT License](https://img.shields.io/github/license/Eutropios/WarMAC)](https://github.com/Eutropios/WarMAC)
[![PyPI](https://img.shields.io/pypi/v/warmac)](https://pypi.org/project/warmac/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warmac)](https://pypi.org/project/warmac/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/warmac)](https://pypi.org/project/warmac/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7670/badge)](https://bestpractices.coreinfrastructure.org/projects/7670)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**WarMAC** is a command-line Python script that can calculate the average market price of items in Warframe.

**WarMAC** compiles orders from the fan website *<https://warframe.market/>*, and can be used to find the average prices of prime parts, tradeable parts, relics, mods, and arcane enhancements.

## 🌟Features

* 🎮Target PC, PlayStation, XBOX, or Nintendo Switch platforms.
* 📈Calculate the median, mean, mode, harmonic mean, or geometric means of items.
* 🕜Restrict orders to specific time ranges.
* 💰Utilize either seller or buyer orders.
* ⛏️Find averages for intact or radiant relics.
* ✨Find averages for unranked or max-ranked mods and arcane enhancements.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Documentation](#documentation)
* [Reporting Issues](#reporting-issues)
* [Upcoming Features](#upcoming-features)
* [Contributing](#contributing)
* [Acknowledgements](#acknowledgements)
* [Licensing](#licensing)

## Installation

WarMAC currently supports Python versions 3.9+. Support for Python 3.8 is planned.

### To install via Pip

Open your terminal and input this command:  
`python -m pip install warmac`

## Usage

Using WarMAC is as simple as:  
`warmac <command> [options] item`

The full command-line usage is as follows:

```txt
usage: warmac <command> [options]

A program to fetch the average market cost of an item in Warframe.

commands:
  average        Calculate the average platinum price of an item.

options:
  -h, --help     Show this message and exit.
  -V, --version  Show the program's version number and exit.
```

## Documentation

Work In Progress.

## Reporting Issues

To report a bug or request a feature, please open an [Issue](https://github.com/Eutropios/WarMAC/issues).

## Upcoming Features

* Adding file I/O
* Adding even more commands to WarMAC!

## Contributing

Contributions are welcome. The expected development stack that you will use is black, mypy, and ruff. Please see [`pyproject.toml`](https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml) for appropriate configuration.

### Testing

There are currently no tests or intrusive Github Actions, but that is expected to change in the future.

## Acknowledgements

In addition to the tools listed in [`.pre-commit-config.yaml`](https://github.com/Eutropios/WarMAC/blob/main/.pre-commit-config.yaml) and [`pyproject.toml`](https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml), this project uses the following tools in its development:

* [autoDocstring](https://github.com/NilsJPWerner/autoDocstring)
* [Even Better TOML](https://github.com/tamasfe/taplo)
* [markdownlint](https://github.com/DavidAnson/vscode-markdownlint)
* [vermin](https://github.com/netromdk/vermin)

WarMAC is packaged using [Poetry](https://github.com/python-poetry/poetry).

## Licensing

***This project is NOT affiliated with Warframe, Digital Extremes, or warframe.market***

Copyright (c) 2023 Noah Jenner under MIT License

*For additional licensing information, please see [`LICENSE.txt`](https://github.com/Eutropios/WarMAC/blob/main/LICENSE.txt)*  
*For licensing regarding urllib3, please see [`LICENSE-urllib3.txt`](https://github.com/Eutropios/WarMAC/blob/main/LICENSE-urllib3.txt)*

## Authors

WarMAC is authored by:

* [@eutropios](https://www.github.com/Eutropios)

[Back to top](#table-of-contents)
