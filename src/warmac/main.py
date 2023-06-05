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

import argparse as ap
import sys
from collections.abc import Callable, Sequence
from datetime import datetime as dt, timezone
from statistics import geometric_mean, harmonic_mean, mean, median, mode

import _classdefs
import _parser
import urllib3

_API_ROOT = "https://api.warframe.market/v1"
_AVG_FUNCS: dict[str, Callable[[Sequence[int]], float]] = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}
CURR_TIME = dt.now(timezone.utc)

headers = {
    "User-Agent": "Mozilla",
    "Content-Type": "application/json",
}

# OrdersList is used to type-hint the json that's returned by using
# .json() on a page returned by a urllib3 http request
OrdersList = list[dict[str, str | int | bool | float | dict[str, int | str | None]]]


# def output(args: ap.Namespace, statistic: float) -> None:
#    pass


def _get_json(url: str) -> urllib3.BaseHTTPResponse:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate headers.
    Raise an error if the status code is not 200.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises _classdefs.UnauthorizedAccessError: Error 401
    :raises _classdefs.ForbiddenRequestError: Error 403
    :raises _classdefs.MalformedURLError: Error 404
    :raises _classdefs.MethodNotAllowedError: Error 405
    :raises _classdefs.InternalServerError: Error 500
    :raises _classdefs.UnknownError: The error is unknown
    :return: The requested page if the status code is 200.
    :rtype: urllib3.BaseHTTPResponse
    """
    page = urllib3.request("GET", url, headers=headers, timeout=5)
    # add 500, 405
    match (page.status):
        case 200:
            return page
        case 401:
            raise _classdefs.UnauthorizedAccessError
        case 403:
            raise _classdefs.ForbiddenRequestError
        case 404:
            raise _classdefs.MalformedURLError
        case 405:
            raise _classdefs.MethodNotAllowedError
        case 500:
            raise _classdefs.InternalServerError
        case _:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Unknown Error; HTTP Code {page.status}")
            raise _classdefs.UnknownError(page.status)


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
    fixed_url = f"{_API_ROOT}/items/{fixed_item}"
    orders: OrdersList = _get_json(f"{fixed_url}/orders").json()["payload"]["orders"]
    print(orders)


_SUBCMD_TO_FUNC: dict[str, Callable[[ap.Namespace], None]] = {
    "average": average,
    # "ducats": None,
    # "lich": None,
    # "riven": None,
    # "sister": None,
    # "graph": None,
    # "popular": None,
    # "costliest": None,
    # "volatile": None
}


def subcommand_select(args: ap.Namespace, /) -> None:
    """
    Select which function to use based on args.subparser field.

    Use try block and a dictionary to execute the appropriate function
    corresponding to the field args.subparser.

    :param args: The argparse Namespace containing the user-supplied
    command line information.
    :type args: ap.Namespace
    :raises _classdefs.SubcommandError: An error indicating that th
    desired subcommand does not exist within the _SUBCMD_TO_FUNC
    dictionary. Is not needed when using the supplied argparser.
    """
    try:
        headers["platform"] = args.platform
        _SUBCMD_TO_FUNC[args.subparser](args)
    except KeyError as err:
        raise _classdefs.SubcommandError from err


def main() -> None:
    """
    Call _parser.handle_input and run subcommand_select with args.

    Call _parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.
    """
    args: ap.Namespace = _parser.handle_input()
    subcommand_select(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting Program.")
