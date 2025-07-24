"""
~~~~~~~~~~~~~~
Warframe Tests
~~~~~~~~~~~~~~

WarMAC — https://github.com/Eutropios/WarMAC
Copyright (C) 2024  Noah Jenner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

-----------------------------------------------------------------------

Obligatory file for unittest to function.
"""  # noqa: D205, D400

from tests import test_average, test_cli_parser, test_fetch_data, test_main

__all__ = ["test_average", "test_cli_parser", "test_fetch_data", "test_main"]
