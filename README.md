<div align="center">

# WarMAC Version 0.0.5

[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Eutropios/WarMAC/main)](https://github.com/Eutropios/WarMAC/commits/main/)
[![Documentation Status](https://readthedocs.org/projects/warmac/badge/?version=latest)](https://warmac.readthedocs.io/en/latest/?badge=latest)\
[![PyPI - Package Version](https://img.shields.io/pypi/v/warmac)](https://pypi.org/project/warmac/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warmac)](https://pypi.org/project/warmac/)\
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MIT License](https://img.shields.io/github/license/Eutropios/WarMAC)](https://github.com/Eutropios/WarMAC)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/warmac)](https://pypi.org/project/warmac/)
[![GitHub issues](https://img.shields.io/github/issues/Eutropios/WarMAC)](https://github.com/Eutropios/WarMAC/issues)

</div>

**WarMAC** is a command-line Python script that can calculate the average market
price of items in Warframe.

**WarMAC** compiles orders from the fan website *<https://warframe.market/>* and
can be used to find the average prices of prime parts, tradeable parts, relics,
mods, and arcane enhancements.

## Features

- 🎮Target PC, PlayStation, XBOX, or Nintendo Switch platforms.
- 📈Calculate the median, mean, mode, harmonic mean, or geometric means of items.
- 🕜Restrict orders to specific time ranges.
- 💰Utilize either seller or buyer orders.
- ⛏️Find averages for intact or radiant relics.
- ✨Find averages for unranked or max-ranked mods and arcane enhancements.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Licensing](#licensing)

## Installation<a id="installation"></a> <!--This ensures PyPI compatibility-->

WarMAC supports Python versions 3.11 to 3.14.

The primary method of installing WarMAC is by installing it through [uv](https://docs.astral.sh/uv/),
though [pipx](https://pypa.github.io/pipx/) may be used as well.
This keeps WarMAC and its dependencies separate from your global Python
packages. Installation can be done using one of the following commands:

### Using uv (or uvx)

The most basic method of installation is by installing as a uv tool like so:

```bash
uv tool install warmac
```

You can ensure that you've installed WarMAC correctly by calling its help page
like so:

```bash
warmac --version
```

### Using pipx

An alternative to installing with uv is pipx:

```bash
pipx install warmac
```

You can ensure that you've installed WarMAC correctly by calling its help page
like so:

```bash
warmac --version
```

### Using pip

Using pip alone to install WarMAC will work just as well, though dependencies
will not be isolated. Installation can be done using the following command:

| Platform | Command |
| --- | --- |
| UNIX/MacOS | `python -m pip install warmac` |
| Windows | `py -m pip install warmac` |

If you're getting an error that `python` is not recognized as a command, try
using the following instead:  
`python3 -m pip install warmac`

You can ensure that you've installed WarMAC correctly by calling its help page
like so:

```bash
warmac --version
```

## Usage<a id="usage"></a>

### General Usage

Full usage instructions as well as examples can be found in the [official documentation](https://warmac.readthedocs.io/en/).

WarMAC has a variety of commands for users to select from. Each command has its
own unique options and arguments. Wherever possible, options that perform
similar functions for different commands will share the same name.

Every WarMAC command is preceded by `warmac`. The general help section of the
program can be viewed by running `warmac --help`.

To view a specific command's usage from the command line, simply run:
`warmac <command> --help`

To view the usage for the average command, users should run:
`warmac average --help`

### Handling WarMAC Output

WarMAC accepts outgoing pipes just like any other tool:

```bash
$ warmac average -p=ps4 -t=5 -d "bite" | grep "Max Price"
Max Price:             65 platinum
```

WarMAC output can also be redirected to a file:

```bash
$ warmac average -p PC -t 2 -d "vengeful revenant" > warmacOut.txt
$ cat warmacOut.txt
Item:                  Vengeful Revenant
Time Range:            2 days
Median Price:          5.0 platinum
Max Price:             30 platinum
Min Price:             4 platinum
Number of Orders:      38 orders
```

### Examples

Calculating the median price of the mod "Primed Continuity" on PS4. Note that
the median is calculated as it's the default.

```bash
warmac average -p ps4 "primed continuity"
```

Calculating the mode price of the mod "Bite" when it's at max rank on PC. Note
that the PC price is calculated as it's the default.

```bash
warmac average -s mode -m bite
```

## Documentation<a id="documentation"></a>

Full documentation for installation, usage, and contribution guidelines can be
found on [WarMAC's readthedocs page](https://warmac.readthedocs.io/en/).

## Contributing<a id="contributing"></a>

Contributions are welcome. Please use the provided pre-commit hooks.

WarMAC is built using [uv](https://docs.astral.sh/uv/). Please use the provided
[`uv.lock`](https://github.com/Eutropios/WarMAC/blob/main/uv.lock) file.

To obtain the source code, you can clone the repository using [git](https://git-scm.com/downloads)
with the following command:

```bash
git clone https://github.com/Eutropios/WarMAC.git ./some/directory
```

WarMAC can then be built by navigating to the directory you cloned WarMAC into,
and running the `uv build` and `uv install` commands.

### Testing

Tests must be run before submitting a PR. Please use the provided `test`
dependency group.

## Acknowledgements<a id="acknowledgements"></a>

This project uses the tools listed in [`.pre-commit-config.yaml`](https://github.com/Eutropios/WarMAC/blob/main/.pre-commit-config.yaml)
and [`pyproject.toml`](https://github.com/Eutropios/WarMAC/blob/main/pyproject.toml)
in its development.

## Licensing<a id="licensing"></a>

***This project is NOT affiliated with Warframe, Digital Extremes, or Warframe Market***

Copyright (C) 2023-2026  Noah Jenner under GNU GPL version 3.0-or-later

*The full details of the license can be found at [`LICENSE.txt`](https://github.com/Eutropios/WarMAC/blob/main/LICENSE)*
*For licensing regarding any dependencies, please see [`LICENSES/](https://github.com/Eutropios/WarMAC/blob/main/LICENSES/)*

## Authors

WarMAC is authored by:

- [@eutropios](https://www.github.com/Eutropios)
