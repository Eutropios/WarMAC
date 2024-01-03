<div align="center">

# WarMAC Version 0.0.5

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Eutropios/WarMAC/main)](https://github.com/Eutropios/WarMAC/commits/main/)
[![Documentation Status](https://readthedocs.org/projects/warmac/badge/?version=latest)](https://warmac.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Eutropios/WarMAC/main.svg)](https://results.pre-commit.ci/latest/github/Eutropios/WarMAC/main)  
[![PyPI - Package Version](https://img.shields.io/pypi/v/warmac)](https://pypi.org/project/warmac/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warmac)](https://pypi.org/project/warmac/)  
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/github/license/Eutropios/WarMAC)](https://github.com/Eutropios/WarMAC)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/warmac)](https://pypi.org/project/warmac/)
[![GitHub issues](https://img.shields.io/github/issues/Eutropios/WarMAC)](https://github.com/Eutropios/WarMAC/issues)

</div>

**WarMAC** is a command-line Python script that can calculate the average market price of items in Warframe.

**WarMAC** compiles orders from the fan website *<https://warframe.market/>* and can be used to find the average prices of prime parts, tradeable parts, relics, mods, and arcane enhancements.

## Features

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
* [Upcoming Features](#upcoming-features)
* [Contributing](#contributing)
* [Acknowledgements](#acknowledgements)
* [Licensing](#licensing)

## Installation<a id="installation"></a> <!--This ensures PyPI compatibility-->

WarMAC only supports Python versions 3.8 to 3.12. There are currently no plans to add support to Python 3.7

### Using pipx

Currently, the primary method of installing WarMAC is by installing it through [pipx](https://pypa.github.io/pipx/). This keeps WarMAC and its dependencies separate from your global Python packages. Installation can be done using the following command:

| Platform | Command |
|---|---|
| UNIX/MacOS | `python -m pipx install warmac` |
| Windows | `py -m pipx install warmac` |

You can ensure that you've installed WarMAC correctly by calling its help page like so:

```bash
warmac --version
```

### Using Pip

Using pip alone to install WarMAC will work just as well. Installation can be done using the following command:

| Platform | Command |
|---|---|
| UNIX/MacOS | `python -m pip install warmac` |
| Windows | `py -m pip install warmac` |

You can ensure that you've installed WarMAC correctly by calling its help page like so:

```bash
warmac --version
```

### Using Poetry

WarMAC can also be installed using [Poetry](https://python-poetry.org/) either through the provided [`poetry.lock`](https://github.com/Eutropios/WarMAC/blob/main/poetry.lock) file (recommended) or by building a lock of your own.

To obtain the source code, you can either download the latest version from [Releases](https://github.com/Eutropios/WarMAC/releases) or by cloning the repository using [git](https://git-scm.com/downloads) with the following command:

```bash
git clone https://github.com/Eutropios/WarMAC.git ./some/directory
```

WarMAC can then be built by navigating to the directory you cloned WarMAC into, and running the `poetry build` and `poetry install` commands.

## Usage<a id="usage"></a>

### General Usage

Full usage instructions as well as examples can be found in the [official documentation](https://warmac.readthedocs.io/en/).

WarMAC has a variety of commands for users to select from. Each command has its own unique options and arguments. Wherever possible, options that perform similar functions for different commands will share the same name.

Every WarMAC command is preceded by ``warmac``. The general help section of the program can be viewed by running `warmac --help`.

To view a specific command's usage from the command line, simply run:
`warmac <command> --help`

For example, to view the usage for the average command, users should run:
`warmac average --help`

### Handling WarMAC Output

WarMAC accepts outgoing pipes just like any other tool:

```bash
$ warmac average -p=ps4 -t=5 -v "bite" | grep "Time Range"
Time Range Used:             10 days
```

WarMAC output can also be redirected to a file:

```bash
$ warmac average -p PC -t 2 -v "vengeful revenant" > warmacOut.txt
$ cat warmacOut.txt
Item:                  Vengeful Revenant
Statistic Found:       Median
Time Range Used:       2 days
Median Price:          5.0 platinum
Max Price:             30 platinum
Min Price:             4 platinum
Number of Orders:      38
```

### Examples

Calculating the median price of the mod "Primed Continuity" on PS4. Note that the median is calculated as it's the default.

```bash
warmac average -p ps4 "primed continuity"
```

Calculating the mode price of the mod "Bite" when it's at max rank on PC. Note that the PC price is calculated as it's the default.

```bash
warmac average -s mode -m bite
```

## Documentation<a id="documentation"></a>

Full documentation for installation, usage, and contribution guidelines can be found [here](https://warmac.readthedocs.io/en/).

## Upcoming Features<a id="upcoming-features"></a>

* Adding file input
* Adding even more commands to WarMAC!

## Contributing<a id="contributing"></a>

Contributions are welcome. The expected development stack that you will use consists of `docformatter`, `mypy`, and `ruff`. Please see [`pyproject.toml`](<https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml>) for the appropriate configuration of each tool.

### Testing

There are currently no tests or intrusive GitHub Actions, but that is expected to change in the future.

## Acknowledgements<a id="acknowledgements"></a>

In addition to the tools listed in [`.pre-commit-config.yaml`](https://github.com/Eutropios/WarMAC/blob/main/.pre-commit-config.yaml) and [`pyproject.toml`](https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml), this project uses the following tools in its development:

* [autoDocstring](https://github.com/NilsJPWerner/autoDocstring)
* [Taplo and the Even Better TOML extension](https://github.com/tamasfe/taplo)
* [markdownlint](https://github.com/DavidAnson/vscode-markdownlint)
* [vermin](https://github.com/netromdk/vermin)

WarMAC is packaged using [Poetry](https://github.com/python-poetry/poetry).

## Licensing<a id="licensing"></a>

***This project is NOT affiliated with Warframe, Digital Extremes, or Warframe Market***

Copyright (c) 2023 Noah Jenner under MIT License

*For additional licensing information, please see [`LICENSE.txt`](https://github.com/Eutropios/WarMAC/blob/main/LICENSE.txt)*  
*For licensing regarding urllib3, please see [`LICENSE-urllib3.txt`](https://github.com/Eutropios/WarMAC/blob/main/LICENSE-urllib3.txt)*

## Authors

WarMAC is authored by:

* [@eutropios](https://www.github.com/Eutropios)
