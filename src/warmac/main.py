"""Warframe Market Average Calculator (WarMAC) 1.5.5
~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all listings of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the listings.

Date of Creation: January 22, 2023
Date Last Modified: May 9, 2023
Version of Python required: 3.10
External packages required: urllib3

UPCOMING:
    Mod rank and Arcane rank handling, show average from buy orders instead of sell orders,
    add drop sources tag, and deleting lowest/highest sell prices to keep average in line
    are coming soon. Possibly adding more average types.
""" # noqa

from datetime import datetime as dt
from datetime import timezone as tz
from statistics import harmonic_mean as harmonic
from statistics import mean, median, mode
import urllib3 as rq
from src.warmac import _arguments

_API_ROOT = "https://api.warframe.market/v1/items"


class _WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self, message: str = "WarMAC Error.") -> None:
        """Construct a WarMAC exception.

        :param message: The message to be printed with the exception, defaults to 'WarMAC Error.'
        :type message: str, optional
        """
        self.message = message
        super().__init__(self.message)


class _AverageTypeError(_WarMACError):
    """Thrown if average type given is not mean, median, mode, or harmonic."""

    def __init__(self) -> None:
        """Construct a _AverageTypeError exception."""
        super().__init__("Not an acceptable average type.")


class _MalformedURLError(_WarMACError):
    """Thrown if there the item name given to WarMAC doesn't exist."""

    def __init__(self) -> None:
        """Construct a _MalformedURLError exception."""
        super().__init__("This item does not exist. Please check your spelling, and remember to use"
                         " parenthesis in the command line if the item is multiple words.")


class _UnknownError(_WarMACError):
    """Thrown if the error is unknown."""

    def __init__(self) -> None:
        """Construct a UnknownError exception."""
        super().__init__("Unknown error, writing to errorLog.txt file. Please open a new issue on"
                         " the Github/Gitlab page (link in README.rst file).")


def _net_error_checking(http_code: int) -> bool:
    """
    Use a switch statement to check the server's response code.

    :param http_code: the status code returned by the GET request
    :type http_code: integer
    :raises _arguments.WarMACError: _description_
    :return: boolean indicating if the GET request was succesful. Returns True if https_code
    is 200, False otherwise
    :rtype: bool
    """
    match http_code:
        case 200:
            return True
        case 404:
            raise _MalformedURLError
        case _:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                print(log_file.write(f"Uknown Error; HTTP Code {http_code}"))
            raise _UnknownError


def _find_avg(plat_list: list, extra: bool = False, avg_type: str = "mean") -> float:
    """
    Given a list, calculate and return the average price in platinum of an item. Extra output can
    be requested by setting `extra` to `True`. `avg_type` must be one of `'mean'`, `'median'`,
    `'mode'`, or `'harmonic'`.

    :param plat_list: list of the prices in platinum of each order
    :type plat_list: list
    :param extra: flag that indicates whether or not to print extra information;
    defaults to False
    :type extra: bool, optional
    :param avg_type: The type of average that the user wants to find. Can be mean, median, mode,
    or harmonic; defaults to 'mean'
    :type avg_type: str, optional
    :raises _AverageTypeError: If given average type isn't mean, median, mode, or harmonic
    :raises ArithmeticError: If given list is empty.
    :return: the average price of all listings of the specified item
    :rtype: float
    """ # noqa
    # Handle errors
    if avg_type not in _arguments.AVG_MODES:
        raise _AverageTypeError
    if not (list_len := len(plat_list)):
        raise ArithmeticError

    # Handle input
    if extra:
        print(f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\tNumber of orders: {list_len}")
    return (
        round(mean(plat_list), 1) if avg_type == "mean" else round(median(plat_list), 1)
        if avg_type == "median" else round(mode(plat_list), 1) if avg_type == "mode" else
        round(harmonic(plat_list), 1)
    )


def _recent_sale(item: dict, time_range: int) -> bool:
    """
    Determine if the listing is a sale, and if it was modified within the last `time_tange` days.

    :param item: Information about a listing
    :type item: dict
    :return: True is the listing was created or modified in the last 60 days is of sell type.
    False if the listing was a buy type or older than 60 days.
    :rtype: bool
    """
    return (
        item["order_type"] == "sell"
        and (dt.now(tz.utc) - dt.fromisoformat(item["last_update"])).days <= time_range
    )


def main() -> None:
    """
    Run WarMAC. ***MUST BE INVOKED FROM COMMAND LINE***.

    Creates argparse parser object and parses the arguments. Appends the user's platform to the
    request header variable (`"pc"` if not specified). Requests json file of orders of user-given
    item from warframe.market and check if the response code is 200. If it is 200, loop through the
    JSON, appending values that return true from `_recent_sale()` to a list. Pass that list along
    with a few other optional arguments from the command line to function `_find_avg()`.
    """
    try:
        args = _arguments.create_parser().parse_args()
        headers = {"User-Agent": "Mozilla", "Content-Type": "application/json",
                   "platform": f"{args.platform}"}
        page = rq.request("GET", f"{_API_ROOT}/{args.item.replace(' ', '_').replace('&', 'and')}"
                          "/orders", headers=headers, timeout=5)
        if _net_error_checking(page.status):
            order_list = [
                order["platinum"]
                for order in page.json()["payload"]["orders"] if _recent_sale(order, args.time_r)
            ]
            result = _find_avg(order_list, args.extra, args.avg_type)
            print(f"The going rate for a {args.item} on {args.platform} is {result:.1f}."
                  if args.verbose else f"{result:.1f}")

    except rq.exceptions.ProtocolError:
        # connection error
        print("You're not connected to the internet. Please check your internet connection"
              " and try again.")
    except ArithmeticError:
        # no orders of that item found
        print("There were no listings of this item found in your specified time range.")
    except _WarMACError as e:
        print(e.message)
