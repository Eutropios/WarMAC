"""
Warframe Market Average Calculator (WarMAC) Beta 0.0.1
~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from
https://warframe.market for a specific platform, then finds the average
price in platinum of the orders.

Date of Creation: January 22, 2023
External packages required: urllib3
"""  # noqa: D205, D400

from __future__ import annotations

import sys
from datetime import datetime, timezone
from statistics import geometric_mean, harmonic_mean, mean, median, mode
from typing import TYPE_CHECKING, Any

import urllib3

from warmac import warmac_errors, warmac_parser

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Callable, Sequence

_API_ROOT: str = "https://api.warframe.market/v1"
AVG_FUNCS: dict[str, Callable[[Sequence[int]], float]] = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}
CURR_TIME: datetime = datetime.now(timezone.utc)

headers = {
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
    "Accept": "application/json",
}


class _WarMACJSON:
    """
    Object storing the contents of a JSON.

    Object that stores the contents of the JSON created using the
    data returned from the HTTP request.
    """

    def __init__(self, json: dict[str, Any]) -> None:
        """
        Construct a _WarMACJSON object.

        :param json: The JSON dictionary that is created from the
        data returned by the HTTP request.
        :type json: dict[str, Any]
        """
        item_info: dict[str, Any] = json["include"]["item"]["items_in_set"][0]
        tags: list[str] = item_info["tags"]
        self.is_relic = "relic" in tags
        self.is_mod_or_arcane = "mod" in tags or "arcane_enhancement" in tags
        self.max_rank = int(item_info["mod_max_rank"]) if self.is_mod_or_arcane else -1
        self.orders: list[dict[str, Any]] = json["payload"]["orders"]

    def __repr__(self) -> str:
        return str(self.orders)


# Load JSON afterwords in average once new version of urllib3 comes out
# which allows type-hinting with BaseHTTPResponse
def _get_page(url: str) -> urllib3.BaseHTTPResponse:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate headers.
    Raise an error if the status code is not 200, otherwise return the
    requested page. This page will need to be decoded into a dictionary.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises warmac_errors.UnauthorizedAccessError: Error 401
    :raises warmac_errors.ForbiddenRequestError: Error 403
    :raises warmac_errors.MalformedURLError: Error 404
    :raises warmac_errors.MethodNotAllowedError: Error 405
    :raises warmac_errors.InternalServerError: Error 500
    :raises warmac_errors.UnknownError: The error is unknown
    :return: The requested page containing a JSON.
    :rtype: urllib3.BaseHTTPResponse
    """
    page = urllib3.request("GET", url, headers=headers, timeout=5)
    status = page.status
    if status == 200:  # noqa: PLR2004
        return page
    if status == 401:  # noqa: PLR2004
        raise warmac_errors.UnauthorizedAccessError
    if status == 403:  # noqa: PLR2004
        raise warmac_errors.ForbiddenRequestError
    if status == 404:  # noqa: PLR2004
        raise warmac_errors.MalformedURLError
    if status == 405:  # noqa: PLR2004
        raise warmac_errors.MethodNotAllowedError
    if status == 500:  # noqa: PLR2004
        raise warmac_errors.InternalServerError
    raise warmac_errors.UnknownError(page.status)


def _calc_avg(plat_list: list[int], statistic: str) -> float:
    """
    Calculate the desired statistic of the price of an item given a
    list of the prices.

    Given a list, calculate and return the average price in platinum of
    an item. Verbose output can be requested by setting args.verbose to
    True.

    :param plat_list: Prices in platinum of each order
    :type plat_list: list[int]
    :param statistic: The statistic to be calculated.
    :type statistic: str
    :raises ArithmeticError: If the given list is empty.
    :return: The desired statistic of the specified item.
    :rtype: float
    """  # noqa: D205
    # Handle errors
    if not plat_list:
        msg = "List cannot be empty!"
        raise ArithmeticError(msg) from None
    try:
        return round(AVG_FUNCS[statistic](plat_list), 1)
    except KeyError as err:
        raise warmac_errors.StatisticTypeError from err


def _in_timerange(last_updated: str, time_range: int) -> bool:
    """
    Check if order is younger than time_range days.

    Subtract last_updated field from CURR_TIME to check if the
    difference in days is less than or equal to time_range.

    :param last_updated: The datetime that the order was last updated.
    :type last_updated: str
    :param time_range: The oldest an order can be to be accepted.
    :type time_range: int
    :return: True if last_updated <= time_range, False if
    last_updated > time_range.
    :rtype: bool
    """
    return (CURR_TIME - datetime.fromisoformat(last_updated)).days <= time_range


def _right_order_type(order_type: str, *, use_buyers: bool = False) -> bool:
    return order_type == ("buy" if use_buyers else "sell")


def _is_max_rank(mod_rank: int, max_rank: int, *, use_maxrank: bool = False) -> bool:
    return mod_rank == (max_rank if use_maxrank else 0)


def _is_radiant(subtype: str, *, use_rad: bool = False) -> bool:
    return subtype == ("radiant" if use_rad else "intact")


def _filter_orders(json: _WarMACJSON, args: Namespace) -> list[int]:
    return [
        order["platinum"]
        for order in json.orders
        if (
            _in_timerange(order["last_update"], args.timerange)
            and _right_order_type(order["order_type"], use_buyers=args.use_buyers)
            and (
                _is_max_rank(order["mod_rank"], json.max_rank, use_maxrank=args.maxrank)
                if json.is_mod_or_arcane
                else True
            )
            and (
                _is_radiant(order["subtype"], use_rad=args.radiant)
                if json.is_relic
                else True
            )
        )
    ]


def verbose_out(avg: float, statistic: str, plat_list: list[int]) -> None:
    """
    Output average price, as well as additional information.

    Output the statistic type, the calculated average price, the
    maximum and minimum values of the list of prices, and the number
    of orders found that match the search criteria. Output the values
    with their corresponding labels preceding them.

    :param avg: The calculated average price of the item.
    :type avg: float
    :param statistic: The statistic that was calculated.
    :type statistic: str
    :param plat_list: A list of all of the platinum prices used in
    the calculation.
    :type plat_list: list[int]
    """
    # {value:{width}.{precision}}
    try:
        space_after_label = 23
        statistic = AVG_FUNCS[statistic].__name__.replace("_", " ").title()
        print(f"{'Statistic Found:':{space_after_label}}{statistic}")
        print(f"{f'{statistic} Price:':{space_after_label}}{avg}")
        print(f"{'Max Price:':{space_after_label}}{max(plat_list)}")
        print(f"{'Min Price:':{space_after_label}}{min(plat_list)}")
        print(f"{'Number of Orders:':{space_after_label}}{len(plat_list)}")
    except KeyError as err:
        raise warmac_errors.StatisticTypeError from err


def average(args: Namespace, /) -> None:
    """
    Determine the specified statistic of an item using command the line
    args supplied by the user.

    Determine the specified statistic of an item using modifiers
    supplied by the user in the command line.

    :param args: The argparse.Namespace containing the user-supplied
    command line information.
    :type args: Namespace
    """  # noqa: D205
    fixed_item: str = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    retrieved_json = _WarMACJSON(_get_page(fixed_url).json())
    plat_list: list[int] = _filter_orders(retrieved_json, args)
    cost = _calc_avg(plat_list, args.statistic)
    verbose_out(cost, args.statistic, plat_list) if args.verbose else print(cost)


_SUBCMD_TO_FUNC: dict[str, Callable[[Namespace], None]] = {
    "average": average,
}


def subcommand_select(args: Namespace, /) -> None:
    """
    Select which function to use based on args.subparser field.

    Use try block and a dictionary to execute the appropriate function
    corresponding to the field args.subparser.

    :param args: The argparse.Namespace containing the user-supplied
    command line information.
    :type args: Namespace
    :raises SubcommandError: An error indicating that the desired
    subcommand does not exist within the _SUBCMD_TO_FUNC dictionary.
    """
    try:
        headers["platform"] = args.platform
        _SUBCMD_TO_FUNC[args.subparser](args)
    except KeyError as err:
        raise warmac_errors.SubcommandError from err
    except warmac_errors.WarMACError as e:
        print(e)
    except urllib3.exceptions.HTTPError as e:
        if isinstance(e, urllib3.exceptions.MaxRetryError):
            print(
                "You're not connected to the internet. Please check your internet "
                "connection and try again.",
            )
        elif isinstance(e, urllib3.exceptions.TimeoutError):
            print("The connection timed out. Please try again later.")
        else:
            print("Unknown connection error.")
    except ArithmeticError:
        print("There are no listings matching your search parameters.")


def main() -> int:
    """
    Call _parser.handle_input and run subcommand_select with args.

    Call _parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.
    """
    args: Namespace = warmac_parser.handle_input()
    subcommand_select(args)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting Program.")
