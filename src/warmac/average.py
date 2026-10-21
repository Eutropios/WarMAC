"""Logic for average subcommand.

-----------------------------------------------------------------------

WarMAC — https://github.com/Eutropios/WarMAC Copyright (C) 2024  Noah
Jenner

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import datetime as dt
import statistics
from dataclasses import dataclass, fields
from typing import TYPE_CHECKING

from warmac import errors, fetch_data, schema

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable, Mapping, Sequence
    from typing import Literal, Self

    AverageType = Literal["geometric", "mean", "median", "mode"]


AVERAGE_FUNCTIONS: Mapping[AverageType, Callable[[Sequence[int]], float]] = {
    "geometric": statistics.geometric_mean,
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
}

# The default number of digits to round to
DEFAULT_NDIGITS = 1

# The default time to collect orders until
DEFAULT_TIME = 3


@dataclass
class AverageNamespace:
    """Store parsed command-line arguments for average calculations.

    Provide a type-aware configuration container for arguments passed
    through the command-line interface, ensuring strict typing.

    Attributes:
        item: Target item for the calculation.
        statistic: Statistical metric to compute.
        timerange: Time range window for the calculation.
        maxrank: Flag or threshold for maximum rank consideration.
        radiant: Radiant status configuration.
        use_buyers: Use buyers instead of sellers.
        ndigits: Number of decimal digits for rounding.
        detailed_report: Flag to enable comprehensive reporting.
        porcelain: Flag to output results in a cleaner format.
    """

    item: str
    statistic: AverageType
    timerange: int
    maxrank: bool
    radiant: Literal["intact", "radiant"]
    use_buyers: Literal["buy", "sell"]
    ndigits: int
    detailed_report: bool
    porcelain: bool

    @classmethod
    def from_namespace(cls, args: argparse.Namespace) -> Self:
        """Transform generic argparse.Namespace into type-aware object.

        Transform the generic argparse.Namespace object into a
        type-aware object. argparse.parse_args creates a type-unaware
        argparse.Namespace object. This loss of type information causes
        function contracts to be less type-safe.

        Args:
            args: Namespace to transform. Must contain all fields
                present in AverageNamespace.

        Returns:
            Fully qualified type-aware object.
        """
        # Filter keys to match only fields defined in the dataclass.
        field_names = {f.name for f in fields(cls)}
        filtered_args = {k: v for k, v in vars(args).items() if k in field_names}
        return cls(**filtered_args)


def calculate_average(
    plat_list: Sequence[int],
    statistic: AverageType,
    ndigits: int = DEFAULT_NDIGITS,
) -> float:
    """Calculate the specified statistic for a list of prices.

    Given a list of integers of prices associated with an item,
    calculate and return the desired statistic, rounded to the specified
    number of decimal places.

    Args:
        plat_list: Prices in platinum of each order.
        statistic: Statistic to be calculated.
        ndigits: Number of decimals to which the calculated statistic
            should be rounded, defaults to 1.

    Returns:
        Desired statistic of the specified item.

    Raises:
        errors.NoListingsFoundError: If ``plat_list`` has no contents.
    """
    if not plat_list:
        raise errors.NoListingsFoundError from None
    return round(float(AVERAGE_FUNCTIONS[statistic](plat_list)), ndigits)


def in_time_range(
    last_updated: str,
    current_time: dt.datetime,
    time_range: int = DEFAULT_TIME,
) -> bool:
    """Check if order is younger than time_range days.

    Subtract ``last_updated`` field from ``current_time`` to check if
    the difference in days is less than or equal to ``time_range``.

    Args:
        last_updated: ISO-8601 timestamp of when the order was last
            updated on Warframe Market.
        current_time: Current UTC time.
        time_range: Maximum age, in days, that an order can be to be
            accepted, defaults to 3.

    Returns:
        True if ``0 <= last_updated ≤ time_range``, False if
        ``last_updated > time_range`` or if ``last_updated < 0``.
    """
    timestamp = dt.datetime.fromisoformat(last_updated)
    return 0 <= (current_time - timestamp).days <= time_range


def check_mod_arcane_rank(
    order_rank: int | None,
    item_max_rank: int | None,
    *,
    use_maxrank: bool,
) -> bool:
    """Check if an order's rank matches user-specified rank level.

    Check if an order's rank equals the rank specified by the user. If
    the item isn't a mod or arcane, ``order_rank`` and ``item_max_rank``
    should both be None. If either ``order_rank`` or ``item_max_rank``
    is None, then True will be returned.

    Args:
        order_rank: Rank of the order.
        item_max_rank: Maximum possible rank for the item.
        use_maxrank: User-specified rank of mod or arcane. If True, the
            maximum potential rank of the item will be use. If False,
            the unranked item will be used.

    Returns:
        True if the ``order_rank`` is None, if ``item_max_rank`` is
        None, or if ``order_rank`` matches
        ``item_max_rank * use_maxrank``, False otherwise.
    """
    if order_rank is None or item_max_rank is None:
        # If there's a mismatch, we'll eval as if unranked
        return True
    return order_rank == (item_max_rank if use_maxrank else 0)


def check_relic_subtype(
    subtype: str | None, refinement: Literal["intact", "radiant"]
) -> bool:
    """Check if an order's subtype matches user-specified refinement.

    Check if an order's subtype equals the refinement level specified by
    the user. If the item isn't a relic, subtype should be None.

    Args:
        subtype: Subtype of the order.
        refinement: User-specified refinement level to compare against.
            Can be either "radiant" or "intact".

    Returns:
        None, False otherwise.
    """
    if subtype is None:
        return True
    return subtype == refinement


def filter_order(
    order: schema.OrderWithUser,
    item_info: schema.Item,
    current_time: dt.datetime,
    args: AverageNamespace,
) -> bool:
    """Check if an order meets all user-specified criteria.

    Check if an order meets all user-defined conditions:

    - Whether the order's last update is within ``args.timerange`` days.
    - Whether the order is of "buy" or "sell" type, depending on
        ``args.use_buyers``.
    - If the item is a mod or arcane, whether its rank is unranked or
        the maximum rank, based on ``args.maxrank``.
    - If the item is a relic, whether its refinement is intact or
        radiant, based on ``args.radiant``.

    Args:
        order: Order to be checked.
        item_info: Details about the item.
        current_time: Current time.
        args: Type-aware, user-given command line arguments.

    Returns:
        True if all specified conditions are met, False otherwise.
    """
    if order.order_type != args.use_buyers:
        return False
    if not check_mod_arcane_rank(
        order.rank, item_info.max_rank, use_maxrank=args.maxrank
    ):
        return False
    if not check_relic_subtype(order.subtype, args.radiant):
        return False
    return in_time_range(order.updated_at, current_time, args.timerange)


def filter_plat_list(
    order_data: Sequence[schema.OrderWithUser],
    item_info: schema.Item,
    current_time: dt.datetime,
    args: AverageNamespace,
) -> list[int]:
    """Construct a list of prices using a filter.

    Return a filtered list of platinum prices given a list of
    ``schema.OrderWithUser``, a ``schema.Item``, and the user's
    command-line arguments.

    Args:
        order_data: List of ``schema.OrderWithUser`` containing
            information about each individual order.
        item_info: Object containing information about the item.
        current_time: Current time.
        args: Type-aware, user-given command line arguments.

    Returns:
        List of the platinum prices from the filtered listings.
    """
    return [
        i.platinum for i in order_data if filter_order(i, item_info, current_time, args)
    ]


def format_output(stat: float, plat_list: Sequence[int], args: AverageNamespace) -> str:
    """Format calculated statistic along with additional information.

    Format the calculated statistic, along with the maximum and minimum
    prices of the orders, and the total number of orders that match the
    search criteria. If ``args.porcelain`` is True, separate the fields
    with a single colon.

    Args:
        stat: Statistic of the item that was found.
        plat_list: List of prices of the item.
        args: Type-aware, user-given command line arguments.

    Returns:
        Return appropriately formatted string.
    """
    # {value:{width}.{precision}}
    if not args.detailed_report:
        return str(stat)
    statistic = AVERAGE_FUNCTIONS[args.statistic].__name__.replace("_", " ").title()
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
        f"{'Number of Orders:':{space_after_label}}{num_orders} orders"
    )


def get_required_data(
    item: str, http_headers: Mapping[str, str]
) -> tuple[schema.ItemResponse, schema.OrderResponse]:
    """Retrieve the orders and metadata for an item.

    Args:
        item: Item to retrieve.
        http_headers: Headers to be used in the HTTP request.

    Returns:
        The item's metadata and the orders associated with it.
    """
    item_data = fetch_data.get_data(item, schema.ItemResponse, http_headers)
    order_data = fetch_data.get_data(item, schema.OrderResponse, http_headers)
    return item_data, order_data


def process_data(
    args: argparse.Namespace,
    http_headers: Mapping[str, str],
    current_time: dt.datetime,
) -> str:
    """Calculate average price of an item from warframe.market.

    Args:
        args: Parsed command-line args. Must have the fields
            ``statistic``, ``item``, ``porcelain``, ``radiant``,
            ``use_buyers``, ``maxrank``, and ``timerange``.
        http_headers: Headers to be used in the HTTP request.
        current_time: Current time.

    Returns:
        Calculated statistic.
    """
    valid_namespace = AverageNamespace.from_namespace(args)
    item_data, order_data = get_required_data(valid_namespace.item, http_headers)
    plat_list = filter_plat_list(
        order_data.data, item_data.data, current_time, valid_namespace
    )
    stat = calculate_average(
        plat_list, valid_namespace.statistic, valid_namespace.ndigits
    )
    return format_output(stat, plat_list, valid_namespace)
