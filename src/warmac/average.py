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

import datetime
import statistics
from typing import TYPE_CHECKING

from warmac import cli_parser, errors, fetch_data, schema

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable, Sequence


AVG_FUNCS: dict[str, Callable[[Sequence[int]], float]] = {
    "geometric": statistics.geometric_mean,
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
}

#: An ISO-8601 timestamp of the current time retrieved on execution.
CURR_TIME = datetime.datetime.now(datetime.timezone.utc)
# When Python 3.10 EOL, change to:
# CURR_TIME = datetime.datetime.now(datetime.UTC)


def calc_avg(plat_list: list[int], statistic: str, decimals: int = 1) -> float:
    """
    Calculate the specified statistic for a list of prices.

    Given a list of integers of prices associated with an item,
    calculate and return the desired statistic, rounded to the specified
    number of decimal places.

    :param plat_list: Prices in platinum of each order.
    :param statistic: Statistic to be calculated.
    :param decimals: Number of decimals to which the calculated
        statistic should be rounded, defaults to 1.
    :raises warmac_errors.NoListingsFoundError: If ``plat_list`` has no
        contents.
    :return: Desired statistic of the specified item.
    """
    # Handle errors
    if not plat_list:
        raise errors.NoListingsFoundError from None
    return round(float(AVG_FUNCS[statistic](plat_list)), decimals)


def in_time_range(last_updated: str, time_range: int = cli_parser.DEFAULT_TIME) -> bool:
    """
    Check if order is younger than ``time_range`` days.

    Subtract last_updated field from :py:data:`.CURR_TIME` to check if
    the difference in days is less than or equal to ``time_range``.

    :param last_updated: ISO-8601 timestamp of when the order was
        last updated.
    :param time_range: Maximum age, in days, that an order can be to
        be accepted, defaults to :py:const:`warmac_parser.DEFAULT_TIME`.
    :return: True if ``last_updated ≤ time_range``, False if
        ``last_updated > time_range``.
    """
    timestamp = datetime.datetime.fromisoformat(last_updated)
    return (CURR_TIME - timestamp).days <= time_range


def filter_order(
    order: schema.OrderWithUser,
    item_info: schema.Item,
    args: argparse.Namespace,
) -> bool:
    """
    Check if an order meets all user-specified criteria.

    Check if an meets all user-defined conditions:

    - Whether the order's last update is within ``args.timerange`` days.
    - Whether the order is of "buy" or "sell" type, depending on
        ``args.use_buyers``.
    - If the item is a mod or arcane, whether its rank is unranked or
        the maximum rank, based on ``args.maxrank``.
    - If the item is a relic, whether its refinement is intact or
        radiant, based on``args.radiant``.

    :param order: Order to be checked.
    :param item_info: Object containing details about the item.
    :param args: Command-line arguments provided by the user.
    :return: True if all specified conditions are met, False otherwise.
    """
    if order.type != args.use_buyers:
        return False
    if (
        order.rank is not None
        and item_info.max_rank is not None
        and order.rank != item_info.max_rank * args.maxrank
    ):
        return False
    if order.subtype is not None and order.subtype != args.radiant:
        return False

    return in_time_range(order.updated_at, args.timerange)


def get_plat_list(
    order_data: list[schema.OrderWithUser],
    item_info: schema.Item,
    args: argparse.Namespace,
) -> list[int]:
    """
    Return a filtered list of platinum prices.

    Return a filtered list of platinum prices given a list of
    :py:class:`schema.OrderWithUser`s, a :py:class:`schema.Item`, and
    the user's command-line arguments.

    :param order_data: List of :py:class:`schema.OrderWithUser`s
        containing information about each individual order.
    :param item_info: Object containing information about the item.
    :param args: User-given command line arguments.
    :return: List of the platinum prices from the filtered listings.
    """
    return [i.platinum for i in order_data if filter_order(i, item_info, args)]


def output(plat_list: list[int], args: argparse.Namespace) -> None:
    """
    Display the average price along with additional information.

    Display the calculated average price, along with the average type
    used, the timerange of the request, the maximum and minimum prices
    of the orders, and the total number of orders that match the search
    criteria.

    :param plat_list: List of prices of the item.
    :param args: User-given command line arguments.
    """
    # {value:{width}.{precision}}
    stat = calc_avg(plat_list, args.statistic, 1)
    if not args.detailed_report:
        print(stat)
    else:
        space_after_label = 23
        statistic = AVG_FUNCS[args.statistic].__name__.replace("_", " ").title()
        fixed_item_name = args.item.title().replace("_", " ").replace(" And ", " & ")
        print(f"{'Item:':{space_after_label}}{fixed_item_name}")
        print(f"{'Statistic Found:':{space_after_label}}{statistic}")
        print(f"{'Time Range Used:':{space_after_label}}{args.timerange} days")
        print(f"{f'{statistic} Price:':{space_after_label}}{stat} platinum")
        print(f"{'Max Price:':{space_after_label}}{max(plat_list):.0f} platinum")
        print(f"{'Min Price:':{space_after_label}}{min(plat_list):.0f} platinum")
        print(f"{'Number of Orders:':{space_after_label}}{len(plat_list)}")


def main(args: argparse.Namespace, http_headers: dict[str, str]) -> None:
    """
    Calculate average price of an item from warframe.market.

    :param args: Parsed command-line args.
    :return: Average price of item.
    """
    # gotta do some error checking here
    item = args.item
    item_data = fetch_data.get_data(item, schema.ItemResponse, http_headers)
    order_data = fetch_data.get_data(item, schema.OrderResponse, http_headers)
    plat_list = get_plat_list(order_data.data, item_data.data, args)
    output(plat_list, args)
