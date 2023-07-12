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

import classdefs
import cli_parser
import urllib3

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


headers = {
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
}

UserInfo = dict[str, int | str | None]
OrdersList = list[dict[str, str | int | bool | float | UserInfo]]
ItemsInSet = list[dict[str, str | int | None | list[str] | dict[str, str]]]
Include = dict[str, str | dict[str, ItemsInSet]]
PageJSON = dict[str, dict[str, OrdersList | Include]]
# def output(args: ap.Namespace, statistic: float) -> None:
#    pass


# Load JSON afterwords in average once new version of urllib3 comes out
# which allows type-hinting with BaseHTTPResponse
def _get_json(url: str) -> Any:  # noqa: ANN401
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate headers.
    Raise an error if the status code is not 200.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises classdefs.UnauthorizedAccessError: Error 401
    :raises classdefs.ForbiddenRequestError: Error 403
    :raises classdefs.MalformedURLError: Error 404
    :raises classdefs.MethodNotAllowedError: Error 405
    :raises classdefs.InternalServerError: Error 500
    :raises classdefs.UnknownError: The error is unknown
    :return: The requested page as a JSON if the status code is 200.
    :rtype: Any
    """
    page = urllib3.request("GET", url, headers=headers, timeout=5)
    match (page.status):
        case 200:
            return page.json()
        case 401:
            raise classdefs.UnauthorizedAccessError
        case 403:
            raise classdefs.ForbiddenRequestError
        case 404:
            raise classdefs.MalformedURLError
        case 405:
            raise classdefs.MethodNotAllowedError
        case 500:
            raise classdefs.InternalServerError
        case _:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Unknown Error; HTTP Code {page.status}")
            raise classdefs.UnknownError(page.status)


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
        raise ArithmeticError(msg)

    # Handle verbosity
    if args.verbose:
        print(
            f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\tNumber of "
            f"orders: {len(plat_list)}"
        )
    return round(AVG_FUNCS[args.statistic](plat_list), 1)


def _filter_orders(args: ap.Namespace) -> float:
    order_list: list[int] = [
        order["platinum"]
        for order in page.json()["payload"]["orders"]
        if (
            in_time_range(order, time_range=args.time_range)
            and correct_order_type(order, use_buyers=args.use_buyers)
        )
    ]
    return _calc_avg(order_list, args)

def _is_mod_or_relic() -> tuple[bool, bool]:
    return (True, True)

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
    fixed_item = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    orders = _get_json(fixed_url)

    _filter_orders(args)


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
    :raises classdefs.SubcommandError: An error indicating that th
    desired subcommand does not exist within the _SUBCMD_TO_FUNC
    dictionary. Is not needed when using the supplied
    argparse.ArgumentParser.
    """
    try:
        headers["platform"] = args.platform
        _SUBCMD_TO_FUNC[args.subparser](args)
    except KeyError:
        raise classdefs.SubcommandError from None


def main() -> int:
    """
    Call parser.handle_input and run subcommand_select with args.

    Call parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.
    """
    args: ap.Namespace = cli_parser.handle_input()
    subcommand_select(args)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting Program.")
