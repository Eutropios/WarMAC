"""
warmac.average
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

Logic for average subcommand.
"""  # noqa: D205, D400

from __future__ import annotations

from typing import TYPE_CHECKING

from warmac import fetch_data, schema

if TYPE_CHECKING:
    import argparse


# Iterate through dictionary and delete all members that do not match
# the parameters set out by args


def main(args: argparse.Namespace, http_headers: dict[str, str]) -> float:
    """
    Calculate average price of an item from warframe.market.

    :param args: Parsed command-line args.
    :return: Average price of item.
    """
    # gotta do some error checking here
    item = args.item
    item_data = fetch_data.get_data(item, schema.ItemResponse, http_headers)
    order_data = fetch_data.get_data(item, schema.OrderResponse, http_headers)
    print(item)  # NOTE: Just debug stuff
    print(f"ITEM DATA:{item_data}\n\n")
    print(f"ORDER DATA:{order_data}")

    # do some validation with msgspec
    return 0.1
