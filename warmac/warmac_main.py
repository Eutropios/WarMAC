"""
Warframe Market Average Calculator (WarMAC) 0.0.4
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
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Sequence

import urllib3

from warmac import warmac_errors, warmac_parser

if TYPE_CHECKING:
    from argparse import Namespace

_API_ROOT = "https://api.warframe.market/v1"
AVG_FUNCS: Dict[str, Callable[[Sequence[int]], float]] = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}
CURR_TIME = datetime.now(timezone.utc)

headers = {
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
    "Accept": "application/json",
}


class _WarMACJSON:
    """
    Object storing the contents of a JSON.

    Object that stores the contents of the JSON created using the data
    returned from the HTTP request.
    """

    def __init__(self, json: Dict[str, Any], /) -> None:
        """
        Construct a _WarMACJSON object.

        Construct a _WarMACJSON object from a decoded JSON returned from
        the http request. Object contains information about if the
        desired item is a mod or arcane (and if so its max rank), or if
        it's a relic. Object also contains the found orders of the item.

        :param json: The JSON dictionary that is created from the data
            returned by the HTTP request.
        :type json: Dict[str, Any]
        :raises KeyError: Raise KeyError if the JSON dictionary does not
            contain the necessary fields for initialization.
        """
        try:
            item_info: Dict[str, Any] = json["include"]["item"]["items_in_set"][0]
            tags: List[str] = item_info["tags"]
            self.is_relic = "relic" in tags
            self.is_mod_or_arcane = "mod" in tags or "arcane_enhancement" in tags
            self.max_rank = (
                int(item_info["mod_max_rank"]) if self.is_mod_or_arcane else -1
            )
            self.orders: List[Dict[str, Any]] = json["payload"]["orders"]
        except KeyError as err:
            msg = "Required JSON field not found."
            raise KeyError(msg) from err

    def __repr__(self) -> str:
        return str(self.orders)

    def __str__(self) -> str:
        return str(self.orders)


# Load JSON afterwords in average once new version of urllib3 comes out
# which allows type-hinting with BaseHTTPResponse
def _get_page(url: str, /) -> urllib3.BaseHTTPResponse:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate headers. Raise
    an error if the status code is not 200, otherwise return the
    requested page. This page will need to be decoded into a dictionary.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises warmac_errors.UnauthorizedAccessError: Error 401.
    :raises warmac_errors.ForbiddenRequestError: Error 403.
    :raises warmac_errors.MalformedURLError: Error 404.
    :raises warmac_errors.MethodNotAllowedError: Error 405.
    :raises warmac_errors.InternalServerError: Error 500.
    :raises warmac_errors.UnknownError: The error is unknown.
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


def _calc_avg(plat_list: List[int], /, statistic: str, *, decimals: int = 1) -> float:
    """
    Calculate the desired statistic of the price of an item.

    Given an integer list of prices associated with an item, calculate
    and return the desired statistic of the price of that item to 1
    decimal point.

    :param plat_list: Prices in platinum of each order.
    :type plat_list: List[int]
    :param statistic: The statistic to be calculated.
    :type statistic: str
    :param decimals: The number of decimals that the statistic should be
        rounded to, defaults to 1.
    :type decimals: int, optional
    :raises warmac_errors.NoListingsFoundError: If plat_list is empty.
    :raises warmac_errors.StatisticTypeError: If statistic is not
        present in AVG_FUNCS.
    :return: The desired statistic of the specified item.
    :rtype: float
    """
    # Handle errors
    if not plat_list:
        raise warmac_errors.NoListingsFoundError from None
    try:
        return round(float(AVG_FUNCS[statistic](plat_list)), decimals)
    except KeyError as err:
        raise warmac_errors.StatisticTypeError from err


def _in_time_r(last_updated: str, /, time_r: int = warmac_parser.DEFAULT_TIME) -> bool:
    """
    Check if order is younger than time_r days.

    Subtract last_updated field from CURR_TIME to check if the
    difference in days is less than or equal to time_r.

    :param last_updated: The datetime that the order was last updated.
    :type last_updated: str
    :param time_r: The oldest an order can be to be accepted, defaults
        to warmac_parser.DEFAULT_TIME.
    :type time_r: int, optional
    :return: True if last_updated <= time_r, False if last_updated >
        time_r.
    :rtype: bool
    """
    return (CURR_TIME - datetime.fromisoformat(last_updated)).days <= time_r


def _right_order_type(order_type: str, *, use_buyers: bool = False) -> bool:
    """
    Check if order_type == "buy" or "sell" depending on use_buyers.

    Check if order_type == "buy" if use_buyers is True, or if order_type
    == "sell" if use_buyers is False.

    :param order_type: The type of the order.
    :type order_type: str
    :param use_buyers: Whether or not order_type should be equal to
        "buy", defaults to False.
    :type use_buyers: bool, optional
    :return: Return order_type == "buy" if use_buyers is True. Return
        order_type == "sell" if use_buyers is False.
    :rtype: bool
    """
    return order_type == ("buy" if use_buyers else "sell")


def _is_max_rank(mod_rank: int, max_rank: int, *, use_maxrank: bool = False) -> bool:
    """
    Check if mod_rank == max_rank or 0 depending on use_buyers.

    Check if mod_rank == max_rank if use_maxrank is True, or if mod_rank
    == 0 if use_maxrank is False.

    :param mod_rank: The rank of the mod or arcane enhancement.
    :type mod_rank: int
    :param max_rank: The max rank of the mod or arcane enhancement.
    :type max_rank: int
    :param use_maxrank: Whether or not to check the mod_rank against the
        max_rank, defaults to False.
    :type use_maxrank: bool, optional
    :return: Return mod_rank == max_rank if use_maxrank is True. Return
        mod_rank == 0 if use_maxrank is False.
    :rtype: bool
    """
    return mod_rank == (max_rank if use_maxrank else 0)


def _is_radiant(subtype: str, *, use_rad: bool = False) -> bool:
    """
    Check if subtype == "radiant" or "intact" depending on use_rad.

    Check if subtype == "radiant" if use_rad is True, or if subtype ==
    "intact" if use_rad is False.

    :param subtype: The subtype of the relic.
    :type subtype: str
    :param use_rad: Whether to check the subtype against "radiant" or
        "intact", defaults to False.
    :type use_rad: bool, optional
    :return: Return subtype == "radiant" if use_rad is True. Return
        subtype == "intact" if use_rad is False.
    :rtype: bool
    """
    return subtype == ("radiant" if use_rad else "intact")


def _filter_order(order: Dict[str, Any], json: _WarMACJSON, args: Namespace, /) -> bool:
    """
    Check if an order meets all specifications given by the user.

    Check if an order meets all user-given specifications by running
    _is_radiant, _in_time_r, _is_max_rank, and _right_order_type.

    :param order: The order to run the checks against.
    :type order: Dict[str, Any]
    :param json: The object containing information about the item.
    :type json: _WarMACJSON
    :param args: The user-given command line arguments.
    :type args: Namespace
    :raises KeyError: If the json does not contain the required fields.
    :return: True if all four functions mentioned return True, returns
        False if any one of them return False.
    :rtype: bool
    """
    try:
        return (
            _right_order_type(order["order_type"], use_buyers=args.use_buyers)
            and _in_time_r(order["last_update"], args.timerange)
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
    except KeyError as err:
        msg = "Required JSON field not found."
        raise KeyError(msg) from err


def _get_plat_list(json: _WarMACJSON, args: Namespace, /) -> List[int]:
    """
    Return a filtered list of platinum prices.

    Return a filtered list of platinum prices given a _WarMACJSON and
    the user's command-line arguments.

    :param json: The object containing the item's listings and the
        associated information with that item.
    :type json: _WarMACJSON
    :param args: The user-given command line arguments.
    :type args: Namespace
    :raises KeyError: If the json does not contain the required fields.
    :return: A list of the platinum prices from the filtered listings.
    :rtype: List[int]
    """
    try:
        return [
            order["platinum"]
            for order in json.orders
            if _filter_order(order, json, args)
        ]
    except KeyError as err:
        msg = "Required JSON field not found."
        raise KeyError(msg) from err


def verbose_out(
    args: Namespace,
    avg_cost: float,
    plat_list: List[int],
    time_r: int = warmac_parser.DEFAULT_TIME,
    /,
) -> None:
    """
    Output average price, as well as additional information.

    Output the statistic type, the calculated average price, the
    timerange of the request, the maximum and minimum values of the list
    of prices, and the total number of orders found that match the
    search criteria. Output the values with their corresponding labels
    preceding them.

    :param args: The user-given command line arguments.
    :type args: Namespace
    :param avg_cost: The statistic of the item that was found.
    :type avg_cost: float
    :param plat_list: The list of prices of the item.
    :type plat_list: List[int]
    :param time_r: The oldest a listing could be to not be filtered out,
        defaults to warmac_parser.DEFAULT_TIME.
    :type time_r: int, optional
    :raises warmac_errors.StatisticTypeError: If statistic is not
        present in AVG_FUNCS.
    """
    # {value:{width}.{precision}}
    try:
        space_after_label = 23
        statistic = AVG_FUNCS[args.statistic].__name__.replace("_", " ").title()
        print(f"{'Item:':{space_after_label}}{args.item.title()}")
        print(f"{'Statistic Found:':{space_after_label}}{statistic}")
        print(f"{'Time Range Used:':{space_after_label}}{time_r}")
        print(f"{f'{statistic} Price:':{space_after_label}}{avg_cost}")
        print(f"{'Max Price:':{space_after_label}}{max(plat_list):.1f}")
        print(f"{'Min Price:':{space_after_label}}{min(plat_list):.1f}")
        print(f"{'Number of Orders:':{space_after_label}}{len(plat_list)}")
    except KeyError as err:
        raise warmac_errors.StatisticTypeError from err


def average(args: Namespace, /) -> None:
    """
    Determine the specified statistic of an item.

    Determine the specified statistic of an item using modifiers
    supplied by the user in the command line.

    :param args: The argparse.Namespace containing the user-supplied
        command line information.
    :type args: Namespace
    """
    fixed_item: str = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    retrieved_json = _WarMACJSON(_get_page(fixed_url).json())
    plat_list: List[int] = _get_plat_list(retrieved_json, args)
    cost = _calc_avg(plat_list, args.statistic)
    verbose_out(
        args,
        cost,
        plat_list,
    ) if args.verbose else print(cost)


_SUBCMD_TO_FUNC: Dict[str, Callable[[Namespace], None]] = {
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
