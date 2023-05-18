"""
Warframe Market Average Calculator (WarMAC) 1.5.8
~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from https://warframe.market for a
specific platform, then finds the average price in platinum of the orders.

Date of Creation: January 22, 2023
Date Last Modified: May 13, 2023
Version of Python required: >=3.7.0
External packages required: urllib3
""" # noqa: D205,D400

import sys
from typing import Any, List, Dict  # REMOVE List AND Dict WHEN 3.7 AND 3.8 SUPPORT ENDS
from datetime import datetime, timezone
import urllib3
try:
    from src.warmac import _arguments
except ImportError:
    import _arguments


_API_ROOT = "https://api.warframe.market/v1/items"
_CURR_TIME = datetime.now(timezone.utc)

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
    Check the server's http response code.

    Raises errors if the http code isn't 200.

    :param http_code: the status code returned by the GET request
    :type http_code: int
    :raises _MalformedURLError: raised if https_code is 404
    :raises _UnknownError: raised if https_Code is not 200 or 404
    :return: boolean indicating if the GET request was successful. Returns True if https_code
    is 200, raises _MalformedURLError if https_code is 404, raises _UnknownError otherwise.
    :rtype: bool
    """
    if http_code == 200:  # noqa: PLR2004
            return True
    if http_code == 404:  # noqa: PLR2004
            raise _MalformedURLError
    with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
        print(log_file.write(f"Unknown Error; HTTP Code {http_code}"))
    raise _UnknownError

def _calc_avg(plat_list: List[int], avg_type: str = "mean", *, extra: bool = False) -> float:
    """
    Calculate the average platinum price of a list of orders using a specific avg_type.

    Given a list, calculate and return the average price in platinum of an item. Extra output can
    be requested by setting extra to True. avg_type must be one of "mean", "median",
    "mode", or "harmonic".

    :param plat_list: list of the prices in platinum of each order
    :type plat_list: list
    :param avg_type: The type of average that the user wants to find. Can be mean, median, mode,
    or harmonic; defaults to 'mean'
    :type avg_type: str, optional
    :param extra: flag that indicates whether or not to print extra information, defaults to False
    :type extra: bool, optional
    :raises ArithmeticError: If given list is empty
    :raises _AverageTypeError: If given average type isn't mean, median, mode, or harmonic
    :return: the average price of all orders of the specified item
    :rtype: float
    """
    # Handle errors
    if not plat_list:
        msg = "List cannot be empty!"
        raise ArithmeticError(msg)
    if avg_type not in _arguments._AVG_FUNCTIONS:
        raise _AverageTypeError

    # Handle input
    if extra:
        print(f"Highest: {max(plat_list)}\tLowest: {min(plat_list)}\tNumber of"
              f" orders: {len(plat_list)}")
    return round(_arguments._AVG_FUNCTIONS[avg_type](plat_list), 1)

def _correct_order_type(item: Dict[str, Any], *, use_buyers: bool = False) -> bool:
    """
    Check if a specific order's order type matches the user-specified order type.

    :param item: Information about a order. Order must include field "order_type".
    :type item: dict
    :param use_buyers: Flag to indicate whether to check for "sell" types or "buy" types,
    defaults to False
    :type use_buyers: bool, optional
    :return: True if the order matched the desired order type. False if did not match.
    :rtype: bool
    """
    return item["order_type"] == ("buy" if use_buyers else "sell")

def _in_time_range(item: Dict[str, Any], time_range: int = 60) -> bool:
    """
    Check if the order's latest modification date was within the past time_range days.

    :param item: Information about a order. Order must include the field "last_update".
    :type item: dict
    :param time_range: The oldest a order can be to return True, defaults to 60
    :type time_range: int, optional
    :return: True if the order was created or modified in the last time_range days. False if the
    order was older than time_range days.
    :rtype: bool
    """
    return  (_CURR_TIME - datetime.fromisoformat(item["last_update"])).days <= time_range

def find_avg() -> None:
    """
    Run logic of WarMAC.

    Creates argparse parser object and parses the arguments. Appends the user's platform to the
    request header variable ("pc" if not specified). Requests json file of orders of user-given
    item from warframe.market and check if the response code is 200. If it is 200, loop through the
    JSON, appending values that return true from _valid_sale() to a list. Pass that list along
    with a few other optional arguments from the command line to function _find_avg().
    """
    args = _arguments._create_parser().parse_args()  # create parser
    headers = {"User-Agent": "Mozilla", "Content-Type": "application/json",
               "platform": f"{args.platform}"}       # add platform to header
    fixed_url = f"{_API_ROOT}/{args.item.replace(' ', '_').replace('&', 'and')}/orders"
    page = urllib3.request("GET", fixed_url, headers=headers, timeout=5)
    if _net_error_checking(page.status):
        order_list: List[int] = [
            order["platinum"]
            for order in page.json()["payload"]["orders"]
            if (_in_time_range(order, args.time_range)
            and _correct_order_type(order, use_buyers=args.use_buyers))
        ]
        result = _calc_avg(order_list, args.avg_type, extra=args.extra)
        print(f"The going rate for a {args.item} on {args.platform} is {result:.1f}."
              if args.verbose else f"{result:.1f}")

def main() -> None:
    """
    Run WarMAC. ***MUST BE INVOKED FROM COMMAND LINE***.

    Handles the errors throughout WarMAC. While the program can be run through find_avg() alone,
    it is recommended that those who use this program's functions implement their own exceptions.
    """
    try:
        find_avg()
    except urllib3.exceptions.HTTPError as e:
        if isinstance(e, urllib3.exceptions.MaxRetryError):
            print("You're not connected to the internet. Please check your internet connection and"
                  " try again.")
        elif isinstance(e, urllib3.exceptions.TimeoutError):
            print("The connection timed out. Please try again later.")
        else:
            print("An error occurred while connecting to the server. Please try again later.")
    except ArithmeticError:
        print("There were no orders of this item found in your specified time range.")
    except _WarMACError as e:
        print(e.message)
    except KeyboardInterrupt:
        print("Exiting program.")

if __name__ == "__main__":
    sys.exit(main())
