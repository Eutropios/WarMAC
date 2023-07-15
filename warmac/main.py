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

import argparse as ap
import shutil
import sys
from datetime import datetime as dt
from datetime import timezone
from statistics import geometric_mean, harmonic_mean, mean, median, mode
from typing import TYPE_CHECKING, Any

import urllib3

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Sequence

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
_DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."
_HELP_MIN_WIDTH = 34
_DEFAULT_WIDTH: int = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
_MAX_TIME_RANGE = 750
_PLATFORMS: tuple[str, str, str, str] = (
    "pc",
    "ps4",
    "xbox",
    "switch",
)
_PROG_NAME = "warmac"
VERSION = "1.6.0"

headers = {
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
}


class WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self: WarMACError, message: str = "WarMAC Error.") -> None:
        """
        Construct a WarMAC exception.

        :param message: The message to be printed with the exception;
        defaults to WarMAC Error.
        :type message: str, optional
        """
        self.message = message
        super().__init__(self.message)


class SubcommandError(WarMACError):
    """
    Thrown if subparser field of argparse.Namespace does not exist
    in SUBCOMMANDS.
    """  # noqa: D205

    def __init__(self: SubcommandError) -> None:
        """Construct a SubcommandError exception."""
        super().__init__("Not a valid subcommand.")


class InternalServerError(WarMACError):
    """
    Thrown if the server has encountered an internal error.

    Thrown on HTTP status code 500, which indicates that server has
    encountered an internal error that prevents it from fulfilling
    the user's request.
    """

    def __init__(self: InternalServerError) -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 500, Warframe.market servers have encountered an "
            "internal error while processing this request."
        )


class MethodNotAllowedError(WarMACError):
    """
    Thrown if the target resource doesn't support the desired method.

    Thrown on HTTP status code 405, which indicates that the server
    knows the method, but the target resource doesn't support it.
    """

    def __init__(self: MethodNotAllowedError) -> None:
        """Construct a MethodNotAllowedError exception."""
        super().__init__(
            "Error 405, the target resource does not support this function."
        )


class MalformedURLError(WarMACError):
    """
    Thrown if there the item name given to WarMAC doesn't exist.

    Thrown on HTTP status code 404, which indicates that the
    resource in question does not exist.
    """

    def __init__(self: MalformedURLError) -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 404, this item does not exist. Please check your spelling, and "
            "remember to use quotations if the item is multiple words."
        )


class ForbiddenRequestError(WarMACError):
    """
    Thrown if the server refuses to authorize a request.

    Thrown on HTTP status code 403, which indicates that access to the
    desired resources is forbidden.
    """

    def __init__(self: ForbiddenRequestError) -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 403, the URL you've requested is forbidden. You do not have"
            " authorization to access it."
        )


class UnauthorizedAccessError(WarMACError):
    """
    Thrown if the user doesn't have the correct credentials.

    Thrown on HTTP status code 401, which indicates that authorization
    via proper user credentials is needed to access this resource.
    """

    def __init__(self: UnauthorizedAccessError) -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 401, insufficient credentials. Please log in to access this content."
        )


class UnknownError(WarMACError):
    """Thrown if the error is unknown."""

    def __init__(self: UnknownError, status_code: int) -> None:
        """Construct a UnknownError exception."""
        super().__init__(
            f"Unknown Error; HTTP Code {status_code}. Writing to errorLog.txt file."
            " Please open a new issue on the Github page (link in README.rst file)."
        )


class _WarMACJSON:
    """
    Object storing the contents of a JSON.

    Object that stores the contents of the JSON created using the
    data returned from the HTTP request.
    """

    def __init__(self: _WarMACJSON, _json: dict[str, Any]) -> None:
        """
        Construct a _WarMACJSON object.

        :param _json: The JSON dictionary that is created from the
        data returned by the HTTP request.
        :type _json: dict[str, Any]
        """
        item_info: dict[str, Any] = _json["include"]["item"]["items_in_set"][0]
        tags: list[str] = item_info["tags"]
        self.is_relic = "relic" in tags
        self.is_mod_or_arcane = "mod" in tags or "arcane_enhancement" in tags
        self.max_mod_rank = item_info["mod_max_rank"] if self.is_mod_or_arcane else -1
        self.orders: list[dict[str, Any]] = _json["payload"]["orders"]

    def __repr__(self: _WarMACJSON) -> str:
        return str(self.orders)


class CustomHelpFormat(ap.RawDescriptionHelpFormatter):
    """
    Custom help formatter for argparse.ArgumentParser.

    Extends argparse.RawDescriptionHelpFormatter. Overrides
    _format_action, _format_action_invocation, and
    _iter_indented_subactions to remove the subcommand metavar tuple,
    remove duplicate option metavar, and correct over-indentation on the
    help menu respectively.
    """

    def __init__(
        self: CustomHelpFormat,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ) -> None:
        """
        Construct a CustomHelpFormat object.

        :param prog: the name of the program
        :type prog: str
        :param indent_increment: how much space should come before the
        options on the help screen, defaults to 2
        :type indent_increment: int, optional
        :param max_help_position: how wide the space between each
        argument and its respective help text should be, defaults to 24
        :type max_help_position: int, optional
        :param width: the total width that the help screen is able to
        occupy in the terminal, defaults to None
        :type width: int | None, optional
        """
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self: CustomHelpFormat, action: ap.Action) -> str:
        """
        Override the superclass _format_action_invocation method.

        Override the superclass' _format_action_invocation method to
        remove the duplicate metavar in the help display for options
        that have both a short form and long form.

        :param action: the action in which to be formatted
        :type action: ap.Action
        :return: the appropriately formatted string
        :rtype: str
        """
        # If option_string is None/zero or nargs is 0
        if not action.option_strings or action.nargs == 0:
            # Return super class' invocation
            return super()._format_action_invocation(action)
        # Otherwise, get the default options metavar
        default: str = self._get_default_metavar_for_optional(action)
        # Assign args_string to _format_args
        args_string: str = self._format_args(action, default)
        # Return the option strings joined with the args_string
        return f"{', '.join(action.option_strings)} {args_string}"

    def _format_action(self: CustomHelpFormat, action: ap.Action) -> str:
        """
        Override the superclass _format_action method.

        Override the superclass' _format_action method to fix the
        indentation of the leading indentation of subparsers on the
        help page.

        :param action: the action in which to be formatted
        :type action: ap.Action
        :return: super's _format_action, formatted with the correct
        leading indentation if the action is a ap._SubParsersAction
        :rtype: str
        """
        # Overrides the superclass _format_action method
        # *Fix indentation for subclasses
        result: str = super()._format_action(action)
        if isinstance(action, ap._SubParsersAction):
            # *Return result with leading spaces removed, and
            # appropriate indentation added.
            return f"{'':{self._current_indent}}{result.lstrip()}"
        return result

    def _iter_indented_subactions(
        self: CustomHelpFormat,
        action: ap.Action,
    ) -> Generator[ap.Action, None, None]:
        """
        Override the superclass _iter_indented_subactions method.

        Override the superclass' _iter_indented_subactions method to
        yield from subactions if the action is a ap._SupParsersAction

        :param action: the action to be yielded from
        :type action: ap.Action
        :yield: actions from a list returned by action._get_subactions
        :rtype: Generator[ap.Action, None, None]
        """
        # Overrides the superclass _iter_indented_subactions method
        # *Fixes indentation on subcommand metavar
        if isinstance(action, ap._SubParsersAction):
            try:
                # *Get reference of subclass
                subactions: Callable[[], list[ap.Action]] = action._get_subactions
            except AttributeError:
                # *If an exception is found, do nothing
                pass
            else:
                # *Yield from the actions list
                yield from subactions()
        else:
            # *Yield from superclass' _iter_indented_subactions method
            yield from super()._iter_indented_subactions(action)


def _int_checking(user_int: str, upper_bound: int) -> int | None:
    """
    Check if input is an integer and is within range.

    Cast input as an integer and raise an argparse.ArgumentTypeError if
    unable to. Raise an argparse.ArgumentTypeError if integer is not
    greater than 0 and less than upper_bounds.

    :param user_int: The user's input
    :type user_int: str
    :param upper_bound: The maximum value that the user's input can be
    :type upper_bound: int
    :raises ValueError: Is thrown if the input is not an integer. Is
    then caught within the function and is raised again as an
    argparse.ArgumentTypeError.
    :raises ap.ArgumentTypeError: Is thrown if the input is not an
    integer, if the integer is less than 0, or if the integer is
    greater than upper_bounds.
    :return: None if the user's input is not an integer or if the user's
    input is not within range. Returns the user's input casted as an
    integer if it's within range.
    :rtype: int | None
    """
    try:
        casted_int = int(user_int)
    except ValueError:
        msg = f"Argument must be an integer greater than 0 and less than {upper_bound}."
        raise ap.ArgumentTypeError(msg) from None
    if not (0 < casted_int <= upper_bound):
        msg = f"Argument must be greater than 0 and less than {upper_bound}."
        raise ap.ArgumentTypeError(msg) from None
    return casted_int


def _create_parser() -> ap.ArgumentParser:
    """
    Create the command-line parser for the program.

    Create the command-line parser using the built-in library argparse.
    Create an argparse.ArgumentParser object and add "help" and
    "version" options to it. Create subparsers for multiple subcommands
    to be used within the program.

    :return: The constructed ArgumentParser object.
    :rtype: ap.ArgumentParser
    """
    parser = ap.ArgumentParser(
        usage=f"{_PROG_NAME} <command> [options]",
        description=_DESCRIPTION,
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,
            max_help_position=_DEFAULT_WIDTH
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
    )
    parser._positionals.title = "commands"

    # ------- Main Parser Arguments -------
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show the program's version number and exit.",
        version=f"{_PROG_NAME} {VERSION}",
    )

    # ======= Sub-Commands =======
    subparsers = parser.add_subparsers(dest="subparser", metavar="")

    # ------- Average -------
    avg_parser: ap.ArgumentParser = subparsers.add_parser(
        "average",
        help="Calculate the average platinum price of an item.",
        description=(
            "Calculate the average platinum price of an item. Able to find the median,"
            " mean, mode, geometric mean, and harmonic mean of the specified item."
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,
            max_help_position=_DEFAULT_WIDTH
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
        usage=(
            f"{_PROG_NAME} average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r]"
            " [-b] [-l] [--color] item"
        ),
    )

    # Option characters used: s, p, r, i, t, b, l, v, h

    # General Namespace on average:
    # Namespace(item='some_item', statistic='median', platform='pc',
    # maxrank=false, timerange=60,
    # use_buyers=False, listings=False, verbose=0)

    avg_parser.add_argument(
        "item",
        type=lambda s: s.strip(),
        help=(
            "Item to find the statistic of. If the item spans multiple words, please"
            " enclose the item within quotation marks."
        ),
    )

    avg_parser.add_argument(
        "-s",
        "--stats",
        default="median",
        type=lambda s: s.lower().strip(),
        choices=AVG_FUNCS,
        help=(
            "Specifies which statistic to return; Can be one of "
            f"[{', '.join(AVG_FUNCS)}]. (Default: median)"
        ),
        metavar="<stat>",
        dest="statistic",
    )

    avg_parser.add_argument(
        "-p",
        "--platform",
        default="pc",
        type=lambda s: s.lower().strip(),
        choices=_PLATFORMS,
        help=(
            "Specifies which platform to fetch orders for; Can be one of "
            f"[{', '.join(_PLATFORMS)}]. (Default: pc)"
        ),
        metavar="<platform>",
    )

    avg_parser.add_argument(
        "-t",
        "--timerange",
        default=DEFAULT_TIME,
        type=lambda x: _int_checking(x, _MAX_TIME_RANGE),
        help=(
            "Specifies in days how old the orders can be. Must be in range [1, "
            f"{_MAX_TIME_RANGE}]. (Default: 60)"
        ),
        metavar="<days>",
        dest="timerange",
    )
    max_or_rad = avg_parser.add_mutually_exclusive_group()

    max_or_rad.add_argument(
        "-m",
        "--maxrank",
        action="store_true",
        help=(
            "Get price statistic of the mod/arcane at max rank instead of at unranked. "
            "(Default: False)"
        ),
        dest="maxrank",
    )

    max_or_rad.add_argument(
        "-r",
        "--radiant",
        action="store_true",
        help=(
            "Get price statistic of the relic at radiant refinement instead of at"
            " intact. (Default: False)"
        ),
        dest="radiant",
    )

    avg_parser.add_argument(
        "-b",
        "--buyers",
        action="store_true",
        help=(
            "Take the average platinum price from buyer orders instead of "
            "from seller orders. (Default: False)"
        ),
        dest="use_buyers",
    )

    avg_parser.add_argument(
        "-l",
        "--listings",
        action="store_true",
        help="Prints all found listings of the specified item.",
        dest="listings",
    )

    avg_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Prints additional information about the program.",
        dest="verbose",
    )

    avg_parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this message and exit.",
    )

    return parser


def handle_input() -> ap.Namespace:
    """
    Create and perform checks on command-line arguments.

    Create argparse.ArgumentParser object, parse command-line arguments,
    and return the parsed arguments as an argparse.Namespace object.

    :return: The parsed command-line arguments.
    :rtype: ap.Namespace
    """
    parser: ap.ArgumentParser = _create_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    parsed_args: ap.Namespace = parser.parse_args()
    # if input validation is true
    return parsed_args


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
            raise UnauthorizedAccessError from None
        case 403:
            raise ForbiddenRequestError from None
        case 404:
            raise MalformedURLError from None
        case 405:
            raise MethodNotAllowedError from None
        case 500:
            raise InternalServerError from None
        case _:
            with open("./errorLog.txt", "a", encoding="UTF-8") as log_file:
                log_file.write(f"Unknown Error; HTTP Code {page.status}")
            raise UnknownError(page.status) from None


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


def _filter_orders(_json: _WarMACJSON, args: ap.Namespace) -> list[int]:
    order_list: list[int] = [
        order["platinum"]
        for order in _json.orders
        if (
            (CURR_TIME - dt.fromisoformat(order["last_update"])).days <= args.timerange
            and order["order_type"] == ("buy" if args.use_buyers else "sell")
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
    fixed_item = args.item.lower().replace(" ", "_").replace("&", "and")
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
    except KeyError as e:
        raise SubcommandError from e
    except WarMACError as e:
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


def main() -> int:
    """
    Call parser.handle_input and run subcommand_select with args.

    Call parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.
    """
    args: ap.Namespace = handle_input()
    subcommand_select(args)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Keyboard Interrupt. Exiting Program.")
