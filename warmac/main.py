#!/usr/bin/python
"""
Warframe Market Average Calculator (WarMAC) 1.5.9
~~~~~~~~~~~~~~~.

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from
https://warframe.market for a specific platform, then finds the average
price in platinum of the orders.

Date of Creation: January 22, 2023
Date Last Modified: June 7, 2023
Version of Python required: >=3.10.0
External packages required: urllib3
"""  # noqa: D205

from __future__ import annotations

import sys
from datetime import datetime as dt
from datetime import timezone
from statistics import geometric_mean, harmonic_mean, mean, median, mode
from typing import TYPE_CHECKING, Any

import urllib3

from warmac import _parser, classdefs

if TYPE_CHECKING:
    import argparse as ap
    from collections.abc import Callable, Sequence

_API_ROOT = "https://api.warframe.market/v1"
AVG_FUNCS: dict[str, Callable[[Sequence[int]], float]] = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}
CURR_TIME = dt.now(timezone.utc)
DEFAULT_TIME = 30

headers = {
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
}


class _WarMACJSON:
    """
    Object storing the contents of a JSON.

    Object that stores the contents of the JSON created using the
    data returned from the HTTP request.
    """

    def __init__(self: _WarMACJSON, order_json: dict[str, Any]) -> None:
        """
        Construct a _WarMACJSON object.

        :param order_json: The JSON dictionary that is created from the
        data returned by the HTTP request.
        :type order_json: dict[str, Any]
        """
        item_info: dict[str, Any] = order_json["include"]["item"]["items_in_set"][0]
        tags: list[str] = item_info["tags"]
        self.is_relic = "relic" in tags
        self.is_mod = "mod" in tags or "arcane_enhancement" in tags
        self.max_rank = int(item_info["mod_max_rank"]) if self.is_mod else -1
        self.orders: list[dict[str, Any]] = order_json["payload"]["orders"]

    def __repr__(self: _WarMACJSON) -> str:
        return str(self.orders)


# def output(args: ap.Namespace, statistic: float) -> None:
#    pass


# Load JSON afterwords in average once new version of urllib3 comes out
# which allows type-hinting with BaseHTTPResponse
def _get_json(url: str) -> _WarMACJSON:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate headers.
    Raise an error if the status code is not 200.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises UnauthorizedAccessError: Error 401
    :raises ForbiddenRequestError: Error 403
    :raises MalformedURLError: Error 404
    :raises MethodNotAllowedError: Error 405
    :raises InternalServerError: Error 500
    :raises UnknownError: The error is unknown
    :return: The requested page as a JSON if the status code is 200.
    :rtype: Any
    """
    page = urllib3.request("GET", url, headers=headers, timeout=5)
    match (page.status):
        case 200:
            return _WarMACJSON(page.json())
        case 401:
            raise classdefs.UnauthorizedAccessError from None
        case 403:
            raise classdefs.ForbiddenRequestError from None
        case 404:
            raise classdefs.MalformedURLError from None
        case 405:
            raise classdefs.MethodNotAllowedError from None
        case 500:
            raise classdefs.InternalServerError from None
        case _:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Unknown Error; HTTP Code {page.status}")
            raise classdefs.UnknownError(page.status) from None


def _calc_avg(plat_list: list[int], args: ap.Namespace) -> float:
    """
    Calculate the desired statistic of the price of an item given a
    list of the prices.

    Given a list, calculate and return the average price in platinum of
    an item. Verbose output can be requested by setting args.verbose to
    True.

    :param plat_list: Prices in platinum of each order
    :type plat_list: list[int]
    :param args: Command-line arguments containing a boolean field for
    verbose output, as well as a boolean field for color.
    :type args: ap.Namespace
    :raises ArithmeticError: If the given list is empty.
    :return: The desired statistic of the specified item.
    :rtype: float
    """  # noqa: D205
    # Handle errors
    if not plat_list:
        msg = "List cannot be empty!"
        raise ArithmeticError(msg) from None

    # Handle verbosity
    if args.verbose:
        print(
            f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\tNumber of "
            f"orders: {len(plat_list)}"
        )
    return round(AVG_FUNCS[args.statistic](plat_list), 1)


def _is_max_rank(
    order_json: _WarMACJSON,
    order: dict[str, Any],
    args: ap.Namespace,
) -> bool:
    mod_rank: int = order["mod_rank"]
    return mod_rank == (order_json.max_rank if args.maxrank else 0)


def _is_radiant(order: dict[str, Any], args: ap.Namespace) -> bool:
    subtype: str = order["subtype"]
    return subtype == ("radiant" if args.radiant else "intact")


def _filter_orders(order_json: _WarMACJSON, args: ap.Namespace) -> list[int]:
    order_list: list[int] = [
        order["platinum"]
        for order in order_json.orders
        if (
            (CURR_TIME - dt.fromisoformat(order["last_update"])).days <= args.timerange
            and order["order_type"] == ("buy" if args.use_buyers else "sell")
            and (_is_max_rank(order_json, order, args) if order_json.is_mod else True)
            and (_is_radiant(order, args) if order_json.is_relic else True)
        )
    ]
    return order_list


def average(args: ap.Namespace, /) -> None:
    """
    Determine the specified statistic of an item using command the line
    args supplied by the user.

    Determine the specified statistic of an item using modifiers
    supplied by the user in the command line.

    :param args: The argparse Namespace containing the user-supplied
    command line information.
    :type args: ap.Namespace
    """  # noqa: D205
    fixed_item: str = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    retrieved_json = _get_json(fixed_url)
    plat_list: list[int] = _filter_orders(retrieved_json, args)
    avg_cost = _calc_avg(plat_list, args)
    print(avg_cost)


_SUBCMD_TO_FUNC: dict[str, Callable[[ap.Namespace], None]] = {
    "average": average,
}


def subcommand_select(args: ap.Namespace, /) -> None:
    """
    Select which function to use based on args.subparser field.

    Use try block and a dictionary to execute the appropriate function
    corresponding to the field args.subparser.

    :param args: The argparse Namespace containing the user-supplied
    command line information.
    :type args: ap.Namespace
    :raises SubcommandError: An error indicating that th
    desired subcommand does not exist within the _SUBCMD_TO_FUNC
    dictionary. Is not needed when using the supplied
    argparse.ArgumentParser.
    """
    try:
        headers["platform"] = args.platform
        _SUBCMD_TO_FUNC[args.subparser](args)
    except KeyError:
        raise classdefs.SubcommandError from None
    except classdefs.WarMACError as e:
        print(e)
    except urllib3.exceptions.HTTPError as e:
        if isinstance(e, urllib3.exceptions.MaxRetryError):
            print(
                "You're not connected to the internet. Please check your internet "
                "connection and try again."
            )
        elif isinstance(e, urllib3.exceptions.TimeoutError):
            print("The connection timed out. Please try again later.")
        else:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Unknown connection error {e}")
            print(f"Unknown connection error {e}. Logged in ./errorLog.txt")
    except ArithmeticError:
        print("There are no listings matching your search parameters.")


def main() -> int:
    """
    Call parser.handle_input and run subcommand_select with args.

    Call parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.
    """
    args: ap.Namespace = _parser.handle_input()
    subcommand_select(args)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting Program.")
