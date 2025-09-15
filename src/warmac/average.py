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

import sys
from typing import TYPE_CHECKING

from warmac import config, errors, fetch_data, schema

if sys.version_info >= (3, 11):
    # NOTE: When Python 3.10 EOL, use datetime instead of dateutil
    from datetime import datetime as dt

    parse = dt.fromisoformat
else:
    import dateutil.parser

    parse = dateutil.parser.parse

if TYPE_CHECKING:
    import argparse
    import datetime
    from typing import Literal


def calculate_average(
    plat_list: list[int],
    statistic: config.AverageKind,
    ndigits: int = config.DEFAULT_NDIGITS,
) -> float:
    """
    Calculate the specified statistic for a list of prices.

    Given a list of integers of prices associated with an item,
    calculate and return the desired statistic, rounded to the specified
    number of decimal places.

    :param plat_list: Prices in platinum of each order.
    :param statistic: Statistic to be calculated.
    :param ndigits: Number of decimals to which the calculated
        statistic should be rounded, defaults to
        :py:const:`config.DEFAULT_NDIGITS`.
    :raises errors.NoListingsFoundError: If ``plat_list`` has no
        contents.
    :return: Desired statistic of the specified item.
    """
    if not plat_list:
        raise errors.NoListingsFoundError from None
    return round(float(config.AVERAGE_FUNCTIONS[statistic](plat_list)), ndigits)


def in_time_range(
    last_updated: str,
    current_time: datetime.datetime,
    time_range: int = config.DEFAULT_TIME,
) -> bool:
    """
    Check if order is younger than ``time_range`` days.

    Subtract last_updated field from current_time to check if the
    difference in days is less than or equal to ``time_range``.

    :param last_updated: ISO-8601 timestamp of when the order was
        last updated.
    :param current_time: Current UTC time.
    :param time_range: Maximum age, in days, that an order can be to
        be accepted, defaults to :py:const:`config.DEFAULT_TIME`.
    :return: True if ``last_updated ≤ time_range``, False if
        ``last_updated > time_range``.
    """
    """
    If sys.version_info >= (3, 11):

    # Use just this when 3.10 eol
        timestamp = datetime.datetime.fromisoformat(last_updated)
    else:
        timestamp = dateutil.parser.parse(last_updated)
    """
    timestamp = parse(last_updated)
    return 0 <= (current_time - timestamp).days <= time_range


def check_mod_arcane_rank(
    order_rank: int | None,
    item_max_rank: int | None,
    *,
    use_maxrank: bool,
) -> bool:
    """
    Check if an order's rank matches user-specified rank level.

    Check if an order's rank equals the rank specified by the user. If
    the item isn't a mod or arcane, ``order_rank`` and ``item_max_rank``
    should both be ``None``. If either ``order_rank`` or
    ``item_max_rank`` is ``None``, then True will be returned.

    :param order_rank: Rank of the order.
    :param item_max_rank: Maximum possible rank for the item.
    :param use_maxrank: User-specified rank of mod or arcane. If True,
        the maximum potential rank of the item will be use. If False,
        the unranked item will be used.
    :return: True if the order_rank is None, if item_max_rank is None,
        or if order's rank matches ``item_max_rank * use_maxrank``,
        False otherwise.
    """
    if order_rank is None or item_max_rank is None:
        # If there's a mismatch, we'll eval as if unranked
        return True
    return order_rank == (item_max_rank if use_maxrank else 0)


def check_relic_subtype(
    subtype: str | None, use_radiant: Literal["intact", "radiant"]
) -> bool:
    """
    Check if an order's subtype matches user-specified refinement level.

    Check if an order's subtype equals the refinement level specified by
    the user. If the item isn't a relic, ``subtype`` should be None.

    :param subtype: Subtype of the order.
    :param use_radiant: User-specified refinement level to compare
        against. Can be either "radiant" or "intact".
    :return: True if the order's subtype matches ``use_radiant`` or if
        subtype is None, False otherwise.
    """
    if subtype is None:
        return True
    return subtype == use_radiant


def filter_order(
    order: schema.OrderWithUser,
    item_info: schema.Item,
    current_time: datetime.datetime,
    args: argparse.Namespace,
) -> bool:
    """
    Check if an order meets all user-specified criteria.

    Check if an order meets all user-defined conditions:

    - Whether the order's last update is within ``args.timerange`` days.
    - Whether the order is of "buy" or "sell" type, depending on
        ``args.use_buyers``.
    - If the item is a mod or arcane, whether its rank is unranked or
        the maximum rank, based on ``args.maxrank``.
    - If the item is a relic, whether its refinement is intact or
        radiant, based on ``args.radiant``.

    :param order: Order to be checked.
    :param item_info: Details about the item.
    :param current_time: Current time.
    :param args: Command-line arguments provided by the user. Must have
        the fields ``use_buyers``, ``maxrank``, ``radiant``, and
        ``timerange``.
    :return: True if all specified conditions are met, False otherwise.
    """
    if order.type != args.use_buyers:
        return False
    if not check_mod_arcane_rank(
        order.rank, item_info.max_rank, use_maxrank=args.maxrank
    ):
        return False
    if not check_relic_subtype(order.subtype, args.radiant):
        return False
    return in_time_range(order.updated_at, current_time, args.timerange)


def filtered_plat_list(
    order_data: list[schema.OrderWithUser],
    item_info: schema.Item,
    current_time: datetime.datetime,
    args: argparse.Namespace,
) -> list[int]:
    """
    Construct a list of prices using a filter.

    Return a filtered list of platinum prices given a list of
    :py:class:`schema.OrderWithUser`, a :py:class:`schema.Item`, and
    the user's command-line arguments.

    :param order_data: List of :py:class:`schema.OrderWithUser`
        containing information about each individual order.
    :param item_info: Object containing information about the item.
    :param current_time: Current time.
    :param args: User-given command line arguments. Must have
        the fields ``statistic``, ``item``, ``porcelain``, and
        ``timerange``.
    :return: List of the platinum prices from the filtered listings.
    """
    return [
        i.platinum for i in order_data if filter_order(i, item_info, current_time, args)
    ]


def format_output(stat: float, plat_list: list[int], args: argparse.Namespace) -> str:
    """
    Format the calculated statistic along with additional information.

    Format the calculated statistic, along with the maximum and minimum
    prices of the orders, and the total number of orders that match the
    search criteria. If ``args.porcelain`` is True, separate the fields
    with a single colon.

    :param stat: Statistic of the item that was found.
    :param plat_list: List of prices of the item.
    :param args: User-given command line arguments. Must have
        the fields ``statistic``, ``item``, ``porcelain``, and
        ``timerange``.
    :return: Return appropriately formatted string.
    """
    # {value:{width}.{precision}}
    if not args.detailed_report:
        return str(stat)
    statistic = (
        config.AVERAGE_FUNCTIONS[args.statistic].__name__.replace("_", " ").title()
    )
    item_name = args.item.title().replace("_", " ").replace(" And ", " & ")
    max_list = max(plat_list)
    min_list = min(plat_list)
    num_orders = len(plat_list)
    if args.porcelain:
        return f"{item_name}:{args.timerange}:{stat}:{min_list}:{max_list}:{num_orders}"

    space_after_label = 23
    return (
        f"{'Item:':{space_after_label}}{item_name}\n"
        f"{'Time Range:':{space_after_label}}{args.timerange} day(s)\n"
        f"{f'{statistic} Price:':{space_after_label}}{stat} platinum\n"
        f"{'Max Price:':{space_after_label}}{max_list:.0f} platinum\n"
        f"{'Min Price:':{space_after_label}}{min_list:.0f} platinum\n"
        f"{'Number of Orders:':{space_after_label}}{num_orders}"
    )


def get_required_data(
    item: str, http_headers: dict[str, str]
) -> tuple[schema.ItemResponse, schema.OrderResponse]:
    """
    Retrieve the orders and metadata for an item.

    :param item: Item to retrieve.
    :param http_headers: Headers to be used in the HTTP request.
    :return: The item's metadata and the orders associated with it.
    """
    item_data = fetch_data.get_data(item, schema.ItemResponse, http_headers)
    order_data = fetch_data.get_data(item, schema.OrderResponse, http_headers)
    return item_data, order_data


def process_data(
    args: argparse.Namespace,
    http_headers: dict[str, str],
    current_time: datetime.datetime,
) -> str:
    """
    Calculate average price of an item from warframe.market.

    :param args: Parsed command-line args. Must have the fields
        ``statistic``, ``item``, ``porcelain``, ``radiant``,
        ``use_buyers``, ``maxrank``, and ``timerange``.
    :param http_headers: Headers to be used in the HTTP request.
    :param current_time: Current time.
    :return: Calculated statistic.
    """
    item_data, order_data = get_required_data(args.item, http_headers)
    plat_list = filtered_plat_list(order_data.data, item_data.data, current_time, args)
    stat = calculate_average(plat_list, args.statistic, args.ndigits)
    return format_output(stat, plat_list, args)


# (WarMAC) $ warmac average foo
# b'{"apiVersion":"0.20.0","data":null,"error":{"request":[
# "app.item.notFound"]}}\n'
# This item does not exist on Warframe Market. Please check your
# spelling and remember to use quotations if the item is multiple words.

# Maybe use these errors instead of urllib3's to do error checking
# Use if statement before second call to determine if needed. Do order
# request first, check for None fields, then check if args want anything
# special, and only then make second request.
# Maybe change the in_time_range to age_limit or something
