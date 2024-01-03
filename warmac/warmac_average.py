"""
warmac.warmac_average
~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the average command for WarMAC.
For information on the main program, please see __init__.py

Date of Creation: January 22, 2023
"""  # noqa: D205, D400

from __future__ import annotations

# Argparse is imported normally to satisfy Sphinx autodoc
import argparse  # noqa: TCH003
import datetime
import statistics
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Sequence,
    TypedDict,
    Union,
)

import urllib3

from warmac import warmac_errors, warmac_parser

#: The root URL used for communicating with the API of warframe.market.
_API_ROOT = "https://api.warframe.market/v1"

# Dict[str, Callable[[Sequence[int]], float]]
#: A dictionary that maps user input to its respective function.
FUNC_MAP: Dict[str, Callable[[Sequence[int]], float]] = {
    "geometric": statistics.geometric_mean,
    "harmonic": statistics.harmonic_mean,
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
}

#: An ISO-8601 timestamp of the current time retrieved on execution.
CURR_TIME = datetime.datetime.now(datetime.timezone.utc)


class _WarMACJSON(TypedDict):
    """
    A :py:class:`~typing.TypedDict` that stores the retrieved JSON.

    A :py:class:`~typing.TypedDict` that stores information about the
    retrieved item, as well as its associated orders.

    :param is_relic: Whether or not the requested item is a relic.
    :param max_rank: The maximum rank that the mod or arcane enhancement
        can be. If the item is not a mod or arcane enhancement, then
        this will store -1.
    :param orders: The requested orders associated with this item.
    """

    is_relic: bool
    max_rank: int
    orders: List[Dict[str, Any]]


def _extract_info(input_json_: Dict[str, Any]) -> _WarMACJSON:
    """
    Extract the necessary information from the retrieved JSON.

    Extract the retrieved item's tags, which indicate whether or not the
    item is a mod, relic, or arcane. If the item is a mod or arcane the
    max rank is stored in max_rank. If the item is not a mod or arcane,
    -1 is stored in max_rank. Finally, a list of dictionaries
    corresponding to each order is also extracted.

    :param input_json_: A decoded JSON obtained from an HTTP request.
    :return: Return a TypedDict containing the information extracted
        from the JSON.
    """
    item_info: Dict[str, Any] = input_json_["include"]["item"]["items_in_set"][0]
    tags: List[str] = item_info["tags"]
    mod_or_arcane = "mod" in tags or "arcane_enhancement" in tags
    json_: _WarMACJSON = {
        "is_relic": "relic" in tags,
        "max_rank": int(item_info["mod_max_rank"]) if mod_or_arcane else -1,
        "orders": input_json_["payload"]["orders"],
    }
    return json_


def get_page(url: str, headers: Dict[str, str]) -> urllib3.BaseHTTPResponse:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from warframe.market using the
    appropriate formatted URL, along with the appropriate headers. Raise
    an error if the status code is not 200, otherwise, return the
    requested page. This page will need to be decoded into a dictionary.

    :param url: The formatted URL of the desired item.
    :param headers: The headers to be used in the HTTP request.
    :raises warmac_errors.UnauthorizedAccessError: Error 401.
    :raises warmac_errors.ForbiddenRequestError: Error 403.
    :raises warmac_errors.MalformedURLError: Error 404.
    :raises warmac_errors.MethodNotAllowedError: Error 405.
    :raises warmac_errors.InternalServerError: Error 500.
    :raises warmac_errors.UnknownError: Any other HTTP status code.
    :return: The requested page containing a JSON.
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


def _calc_avg(plat_list: List[int], statistic: str, decimals: int = 1) -> float:
    """
    Calculate the desired statistic of the price of an item.

    Given an integer list of prices associated with an item, calculate
    and return the desired statistic of the price of that item to 1
    decimal point.

    :param plat_list: Prices in platinum of each order.
    :param statistic: The statistic to be calculated.
    :param decimals: The number of decimals that the statistic should be
        rounded to, defaults to 1.
    :raises warmac_errors.NoListingsFoundError: If ``plat_list`` has no
        contents.
    :return: The desired statistic of the specified item.
    """
    # Handle errors
    if not plat_list:
        raise warmac_errors.NoListingsFoundError from None
    return round(float(FUNC_MAP[statistic](plat_list)), decimals)


def _in_time_r(last_updated: str, time_r: int = warmac_parser.DEFAULT_TIME) -> bool:
    """
    Check if order is younger than ``time_r`` days.

    Subtract last_updated field from :py:data:`.CURR_TIME` to check if
    the difference in days is less than or equal to ``time_r``.

    :param last_updated: The date and time that the order was last
        updated at.
    :param time_r: The oldest an order can be to be accepted, defaults
        to :py:const:`warmac_parser.DEFAULT_TIME`.
    :return: True if ``last_updated ≤ time_r``, False if ``last_updated
        > time_r``.
    """
    return (CURR_TIME - datetime.datetime.fromisoformat(last_updated)).days <= time_r


def _comp_val(
    val: Union[str, int],
    true_val: Union[str, int],
    false_val: Union[str, int],
    *,
    condition: bool = False,
) -> bool:
    """
    Compare the value ``val`` with either ``true_val`` or ``false_val``
    based on a given true or false ``condition``.

    :param val: The value to be compared.
    :param true_val: The value to be used if ``condition`` is True.
    :param false_val: The value to be used if ``condition`` is False.
    :param condition: The condition to determine which value to use,
        defaults to False.
    :return: True if ``val`` is equal to ``true_val``, False if ``val``
        is equal to ``false_val``.
    """  # noqa: D205
    return val == (true_val if condition else false_val)


def _filter_order(
    order: Dict[str, Any],
    json_: _WarMACJSON,
    args: argparse.Namespace,
) -> bool:
    """
    Check if an order meets all specifications given by the user.

    Check if an order meets all user-given specifications which are as
    follows:

    - if it was updated less than ``args.timerange`` days ago
    - if the order is of type "buy" or "sell" depending on
      ``args.use_buyers``
    - if the order is a mod or arcane, whether it's unranked or max rank
      depending on ``args.maxrank``
    - if the order is a relic, whether it's intact or radiant depending
      on ``args.radiant``

    :param order: The order to run the checks against.
    :param json_: The object containing information about the item.
    :param args: The user-given command line arguments.
    :return: True if all four conditions are met, return False if any
        one of them are not met.
    """
    return (
        # Check if the order type is a buy or sell order depending
        # on args.use_buyers
        _comp_val(order["order_type"], "buy", "sell", condition=args.use_buyers)
        and _in_time_r(order["last_update"], args.timerange)
        and (
            # Check if the rank of the mod is the mod's max rank or
            # unranked depending on args.maxrank
            _comp_val(order["mod_rank"], json_["max_rank"], 0, condition=args.maxrank)
            if json_["max_rank"] != -1
            else True
        )
        and (
            # Check if the refinement of the relic is "radiant" or
            # "intact" depending on args.radiant
            _comp_val(order["subtype"], "radiant", "intact", condition=args.radiant)
            if json_["is_relic"]
            else True
        )
    )


def _get_plat_list(json_: _WarMACJSON, args: argparse.Namespace) -> List[int]:
    """
    Return a filtered list of platinum prices.

    Return a filtered list of platinum prices given a
    :py:class:`._WarMACJSON` and the user's command-line arguments.

    :param json_: The object containing the item's listings and the
        associated information with that item.
    :param args: The user-given command line arguments.
    :return: A list of the platinum prices from the filtered listings.
    """
    return [
        order["platinum"]
        for order in json_["orders"]
        if _filter_order(order, json_, args)
    ]


def _verbose_out(
    args: argparse.Namespace,
    avg_cost: float,
    plat_list: List[int],
) -> None:
    """
    Display the average price along with additional information.

    Display the calculated average price, along with the average type
    used, the timerange of the request, the maximum and minimum prices
    of the orders, and the total number of orders that match the search
    criteria.

    :param args: The user-given command line arguments.
    :param avg_cost: The statistic of the item that was found.
    :param plat_list: The list of prices of the item.
    """
    # {value:{width}.{precision}}
    space_after_label = 23
    statistic = FUNC_MAP[args.statistic].__name__.replace("_", " ").title()
    fixed_item_name = args.item.title().replace("_", " ").replace(" And ", " & ")
    print(f"{'Item:':{space_after_label}}{fixed_item_name}")
    print(f"{'Statistic Found:':{space_after_label}}{statistic}")
    print(f"{'Time Range Used:':{space_after_label}}{args.timerange} days")
    print(f"{f'{statistic} Price:':{space_after_label}}{avg_cost} platinum")
    print(f"{'Max Price:':{space_after_label}}{max(plat_list):.0f} platinum")
    print(f"{'Min Price:':{space_after_label}}{min(plat_list):.0f} platinum")
    print(f"{'Number of Orders:':{space_after_label}}{len(plat_list)}")


def average(args: argparse.Namespace) -> None:
    """
    Determine the specified statistic of an item.

    Determine the specified statistic of an item using modifiers
    supplied by the user in the command line.

    :param args: The :py:class:`argparse.Namespace` containing the
        user-supplied command line information.
    """
    headers: Dict[str, str] = {
        "Accept": "application/json",
        "Accept-Language": "en",
        "Content-Type": "application/json",
        "Host": "api.warframe.market",
        "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
        "Platform": args.platform,
    }
    fixed_item: str = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    plat_list = _get_plat_list(_extract_info(get_page(fixed_url, headers).json()), args)
    cost = _calc_avg(plat_list, args.statistic)
    _verbose_out(
        args,
        cost,
        plat_list,
    ) if args.verbose else print(cost)
