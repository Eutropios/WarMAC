"""
Warframe Market Average Calculator (WarMAC) 1.5.9
~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from https://warframe.market
for a specific platform, then finds the average price in platinum of the orders.

Date of Creation: January 22, 2023
Date Last Modified: June 4, 2023
Version of Python required: >=3.9.0
External packages required: urllib3
"""  # noqa: D205,D400

from __future__ import annotations

import string
import sys
import typing
from datetime import datetime, timezone
import urllib3

try:
    from src.warmac import _arguments  # type: ignore
    from src.warmac import _classdefs
except ImportError:
    import _arguments  # type: ignore
    import _classdefs  # type: ignore
if typing.TYPE_CHECKING:
    import argparse

_API_ROOT = "https://api.warframe.market/v1/"
_CURR_TIME = datetime.now(timezone.utc)


def _net_error_checking(
    http_code: int,
    /,
) -> bool:
    """
    Check the server's http response code.

    Check the server's http response code and returns True if it's equal to 200.
    Function raises errors if the http code isn't 200.

    :param http_code: the status code returned by the GET request
    :type http_code: int
    :raises _MalformedURLError: raised if https_code is 404
    :raises _UnknownError: raised if https_Code is not 200 or 404
    :return: boolean indicating if the GET request was successful. Returns True if
    https_code is 200, raises _MalformedURLError if https_code is 404, raises
    _UnknownError otherwise.
    :rtype: bool
    """
    if http_code == 200:  # noqa: PLR2004
        return True
    if http_code == 404:  # noqa: PLR2004
        raise _classdefs.MalformedURLError
    with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
        log_file.write(f"Unknown Error; HTTP Code {http_code}")
        print(f"Unknown Error; HTTP Code {http_code}. Logged in ./errorLog.txt")
    raise _classdefs.UnknownError


def _calc_avg(
    plat_list: list[int],
    *,
    avg_type: str = "mean",
) -> float:
    """
    Calculate the average platinum price of a list of orders using a specific avg_type.

    Given a list, calculate and return the average price in platinum of an item. Extra
    output can be requested by setting extra to True. avg_type must be one of "mean",
    "median", "mode", or "harmonic".

    :param plat_list: prices in platinum of each order
    :type plat_list: list[int]
    :param avg_type: type of average to calculate. Can be one of mean, median, mode,
    or harmonic; defaults to mean
    :type avg_type: str, optional
    :raises ArithmeticError: If given list is empty
    :raises _AverageTypeError: If avg_type isn't in _arguments.AVG_FUNCS
    :return: the average price of all orders of the specified item
    :rtype: float
    """
    # Handle errors
    if not plat_list:
        msg = "List cannot be empty!"
        raise ArithmeticError(msg)
    if avg_type not in _arguments.AVG_FUNCS:
        raise _classdefs.AverageTypeError

    # Handle input
    print(
        f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\tNumber of "
        f"orders: {len(plat_list)}"
    )
    return round(_arguments.AVG_FUNCS[avg_type](plat_list), 1)  # type: ignore


def _correct_order_type(
    item: dict[str, str],
    *,
    use_buyers: bool = False,
) -> bool:
    """
    Check if a specific order's order type matches the user-specified order type.

    Check the "other_type" field of the specific order against the parameter
    use_buyers to determine if the order type is correct.

    :param item: Information about a order. Order must include field "order_type".
    :type item: dict[str, str]
    :param use_buyers: Flag to indicate whether to check for "sell" types or "buy"
    types, defaults to False
    :type use_buyers: bool, optional
    :return: True if the order matched the desired order type. False if did not match.
    :rtype: bool
    """
    return item["order_type"] == ("buy" if use_buyers else "sell")


def _in_time_range(
    item: dict[str, str],
    *,
    time_range: int = 60,
) -> bool:
    """
    Check if a specific order's "last_update" date was within the past time_range days.

    Use the "last_update" field of the specific order along with the current day to
    find the difference in dates. Return True if date difference is less than the
    time_range parameter, return False if it is not.

    :param item: Information about a order. Order must include the field "last_update".
    :type item: dict[str, str]
    :param time_range: The oldest a order can be to return True; defaults to 60
    :type time_range: int, optional
    :return: True if the order was created or modified in the last time_range days.
    False if the order was older than time_range days.
    :rtype: bool
    """
    return (_CURR_TIME - datetime.fromisoformat(item["last_update"])).days <= time_range


def find_avg(
    args: "argparse.Namespace",  # noqa: UP037
    fixed_url: str,
    /,
) -> None:
    """
    Run logic of WarMAC. ***Must be called with an already parsed argparse object***.

    Append the user's platform to the request header variable ("pc" if not specified).
    Request json file of orders of user-given item from warframe.market and check if
    the response code is 200. If it is 200, loop through the JSON, appending values
    that return true from _valid_sale() to a list. Pass that list along with a few
    other optional arguments from the command line to function _calc_avg().
    """
    headers = {
        "User-Agent": "Mozilla",
        "Content-Type": "application/json",
        "platform": f"{args.platform}",
    }

    page = urllib3.request(
        "GET",
        f"{_API_ROOT}items/{fixed_url}/orders",
        headers=headers,
        timeout=5,
    )
    if _net_error_checking(page.status):
        order_list: list[int] = [
            order["platinum"]
            for order in page.json()["payload"]["orders"]
            if (
                _in_time_range(order, time_range=args.time_range)
                and _correct_order_type(order, use_buyers=args.use_buyers)
            )
        ]
        result = _calc_avg(order_list, avg_type=args.avg_type)
        print(
            f"The {args.avg_type} for a {string.capwords(args.item)} on {args.platform}"
            f" is {result:.1f}."
        )


def main() -> int:
    """
    Run WarMAC. ***MUST BE INVOKED FROM COMMAND LINE***.

    Handles the errors throughout WarMAC. While the program can be run through
    find_avg() alone, it is recommended that those who use this program's functions
    implement their own exceptions.
    """
    try:
        args = _arguments.create_parser().parse_args()  # create parser
        fixed_name = args.item.lower().replace(" ", "_").replace("&", "and")
        find_avg(args, fixed_name)

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
        print("There were no orders of this item found in your specified time range.")
    except _classdefs.WarMACError as e:
        print(e.message)
    except KeyboardInterrupt:
        print("Exiting program.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
