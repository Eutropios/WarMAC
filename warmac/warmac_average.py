"""
warmac.warmac_average
~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the average subcommand for WarMAC.
For information on the main program, please see __init__.py

Date of Creation: January 22, 2023
External packages required: urllib3
"""  # noqa: D205, D400

from __future__ import annotations

from datetime import datetime, timezone
from statistics import geometric_mean, harmonic_mean, mean, median, mode
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Sequence, Union

import urllib3

from warmac import warmac_errors, warmac_parser

if TYPE_CHECKING:
    from argparse import Namespace

# The root URL used for communicating with the API of warframe.market.
_API_ROOT = "https://api.warframe.market/v1"

# A dictionary that maps user input to its respective function.
AVG_FUNCS: Dict[str, Callable[[Sequence[int]], float]] = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "geometric": geometric_mean,
    "harmonic": harmonic_mean,
}

# An ISO-8601 timestamp of the current time retrieved on execution.
CURR_TIME = datetime.now(timezone.utc)

# A dictionary containing the headers to be used in the HTTP request.
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
        Construct a :py:class:`._WarMACJSON` object.

        Construct a :py:class:`._WarMACJSON` object using a decoded JSON
        returned from a HTTP request. Object contains information about
        if the desired item is a mod or arcane (and if so its max rank),
        or if it's a relic. Object also contains the found orders of the
        item.

        :param json: The JSON dictionary that is created from the data
            returned by the HTTP request.
        :type json: Dict[str, Any]
        :raises KeyError: If the JSON dictionary does not contain the
            necessary fields for initialization.
        """
        item_info: Dict[str, Any] = json["include"]["item"]["items_in_set"][0]
        tags: List[str] = item_info["tags"]
        self.is_relic = "relic" in tags
        self.is_mod_or_arcane = "mod" in tags or "arcane_enhancement" in tags
        self.max_rank = int(item_info["mod_max_rank"]) if self.is_mod_or_arcane else -1
        self.orders: List[Dict[str, Any]] = json["payload"]["orders"]

    def __repr__(self) -> str:
        return str(self.orders)

    def __str__(self) -> str:
        return str(self.orders)


def _get_page(url: str, /) -> urllib3.BaseHTTPResponse:
    """
    Request the JSON of a desired item from Warframe.Market.

    Request the JSON of a desired item from Warframe.Market using the
    appropriate formatted URL, along with the appropriate
    :py:data:`.headers`. Raise an error if the status code is not 200,
    otherwise return the requested page. This page will need to be
    decoded into a dictionary.

    :param url: The formatted URL of the desired item.
    :type url: str
    :raises warmac_errors.UnauthorizedAccessError: Error 401.
    :raises warmac_errors.ForbiddenRequestError: Error 403.
    :raises warmac_errors.MalformedURLError: Error 404.
    :raises warmac_errors.MethodNotAllowedError: Error 405.
    :raises warmac_errors.InternalServerError: Error 500.
    :raises warmac_errors.UnknownError: Any other HTTP status code not
        covered by the previous exceptions.
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


def _calc_avg(plat_list: List[int], /, statistic: str, *, decimals: int = 1) -> float:
    """
    Calculate the desired ``statistic`` of the price of an item.

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
    :raises warmac_errors.NoListingsFoundError: If ``plat_list`` has no
        contents.
    :raises warmac_errors.StatisticTypeError: If ``statistic`` is not
        present in :py:data:`.AVG_FUNCS`.
    :return: The desired statistic of the specified item.
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
    Check if order is younger than ``time_r`` days.

    Subtract last_updated field from :py:const:`.CURR_TIME` to check if
    the difference in days is less than or equal to ``time_r``.

    :param last_updated: The date and time that the order was last
        updated at.
    :type last_updated: str
    :param time_r: The oldest an order can be to be accepted, defaults
        to :py:const:`warmac_parser.DEFAULT_TIME`.
    :type time_r: int, optional
    :return: True if ``last_updated ≤ time_r``, False if ``last_updated
        > time_r``.
    """
    return (CURR_TIME - datetime.fromisoformat(last_updated)).days <= time_r


def _comp_val(
    val_to_comp: Union[str, int],
    true_val: Union[str, int],
    false_val: Union[str, int],
    *,
    condition: bool = False,
) -> bool:
    """
    Check if ``val_to_comp`` equals ``true_val`` or ``false_val``.

    Check if ``val_to_comp == true_val`` if ``condition`` is True, or if
    ``val_to_comp == false_val`` if ``condition`` is False.

    :param val_to_comp: The string to check against.
    :type val_to_comp: Union[str, int]
    :param true_val: The string that ``val_to_comp`` will be checked
        against if ``condition`` is True.
    :type true_val: Union[str, int]
    :param false_val: The string that ``val_to_comp`` will be checked
        against if ``condition`` is False.
    :type false_val: Union[str, int]
    :param condition: Whether to check ``val_to_comp`` against
        ``true_val`` or ``false_val``, defaults to False.
    :type condition: bool, optional
    :return: Return ``val_to_comp == true_val`` if ``condition`` is
        True. Return ``val_to_comp == false_val`` if ``condition`` is
        False.
    """
    return val_to_comp == (true_val if condition else false_val)


def _filter_order(order: Dict[str, Any], json: _WarMACJSON, args: Namespace, /) -> bool:
    """
    Check if an order meets all specifications given by the user.

    Check if an order meets all user-given specifications which are as
    follows:

    * if it was updated less than ``args.timerange`` days ago
    * if the order is of type "buy" or "sell" depending on
      ``args.use_buyers``
    * if the order is a mod or arcane, whether it's unranked or max rank
      depending on ``args.maxrank``
    * if the order is a relic, wether it's intact or radiant depending
      on ``args.radiant``

    :param order: The order to run the checks against.
    :type order: Dict[str, Any]
    :param json: The object containing information about the item.
    :type json: _WarMACJSON
    :param args: The user-given command line arguments.
    :type args: argparse.Namespace
    :raises KeyError: If ``json`` does not contain the required fields.
    :return: True if all four conditions are met, return False if any
        one of them are not met.
    """
    try:
        return (
            # Check if the order type is a buy or sell order depending
            # on args.use_buyers
            _comp_val(order["order_type"], "buy", "sell", condition=args.use_buyers)
            and _in_time_r(order["last_update"], args.timerange)
            and (
                # Check if the rank of the mod is the mod's max rank or
                # unranked depending on args.maxrank
                _comp_val(order["mod_rank"], json.max_rank, 0, condition=args.maxrank)
                if json.is_mod_or_arcane
                else True
            )
            and (
                # Check if the refinement of the relic is "radiant" or
                # "intact" depending on args.radiant
                _comp_val(order["subtype"], "radiant", "intact", condition=args.radiant)
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

    Return a filtered list of platinum prices given a
    :py:class:`._WarMACJSON` and the user's command-line arguments.

    :param json: The object containing the item's listings and the
        associated information with that item.
    :type json: _WarMACJSON
    :param args: The user-given command line arguments.
    :type args: argparse.Namespace
    :raises KeyError: If ``json`` does not contain the required fields.
    :return: A list of the platinum prices from the filtered listings.
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


def _verbose_out(
    args: Namespace,
    avg_cost: float,
    plat_list: List[int],
    /,
    time_r: int = warmac_parser.DEFAULT_TIME,
) -> None:
    """
    Output average price, as well as additional information.

    Output the statistic type, the calculated average price, the
    timerange of the request, the maximum and minimum values of the list
    of prices, and the total number of orders found that match the
    search criteria. Output the values with their corresponding labels
    preceding them.

    :param args: The user-given command line arguments.
    :type args: argparse.Namespace
    :param avg_cost: The statistic of the item that was found.
    :type avg_cost: float
    :param plat_list: The list of prices of the item.
    :type plat_list: List[int]
    :param time_r: The oldest a listing could be to not be filtered out,
        defaults to :py:const:`warmac_parser.DEFAULT_TIME`.
    :type time_r: int, optional
    :raises warmac_errors.StatisticTypeError: If ``statistic`` is not
        present in :py:data:`.AVG_FUNCS`.
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

    :param args: The :py:class:`argparse.Namespace` containing the
        user-supplied command line information.
    :type args: argparse.Namespace
    """
    headers["platform"] = args.platform
    fixed_item: str = args.item.lower().replace(" ", "_").replace("&", "and")
    fixed_url = f"{_API_ROOT}/items/{fixed_item}/orders?include=item"
    retrieved_json = _WarMACJSON(_get_page(fixed_url).json())
    plat_list: List[int] = _get_plat_list(retrieved_json, args)
    cost = _calc_avg(plat_list, args.statistic)
    _verbose_out(
        args,
        cost,
        plat_list,
    ) if args.verbose else print(cost)
