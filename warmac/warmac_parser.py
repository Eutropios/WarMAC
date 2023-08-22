"""
warmac.warmac_parser
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the argument parser for WarMAC.
For information on the main program, please see main.py

Date of Creation: June 7, 2023
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import contextlib
import shutil
import sys
from typing import TYPE_CHECKING, NoReturn, Union

from warmac import warmac_errors

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

AVG_FUNCS = ("median", "mean", "mode", "harmonic", "geometric")
DEFAULT_TIME = 10
_HELP_MIN_WIDTH = 34
_DEFAULT_WIDTH = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
_MAX_TIME_RANGE = 60
_PLATFORMS = ("pc", "ps4", "xbox", "switch")


class CustomHelpFormat(argparse.RawDescriptionHelpFormatter):
    """
    Custom help formatter for WarMACParser.

    Extend argparse.RawDescriptionHelpFormatter to override
    _format_action, _format_action_invocation, and
    _iter_indented_subactions. Overrides remove the subcommand metavar
    tuples, remove the duplicate option metavars, and correct the over-
    indentation on the help menu respectively.
    """

    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: Union[int, None] = None,
    ) -> None:
        """
        Construct a CustomHelpFormat object.

        :param prog: The name of the program.
        :type prog: str
        :param indent_increment: How much space should come before the
            options on the help screen, defaults to 2.
        :type indent_increment: int, optional
        :param max_help_position: The width between indent_increment and
            the help text, defaults to 24.
        :type max_help_position: int, optional
        :param width: The maximum width that the help screen is able to
            occupy in the terminal, defaults to None.
        :type width: Union[int, None], optional
        """
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Remove duplicate metavar for options with short and long form.

        Override the _format_action_invocation method to remove the
        duplicate help metavar for options that have both a short form
        and long form argument.

        :param action: The action in which to be formatted.
        :type action: argparse.Action
        :return: The appropriately formatted string.
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

    def _format_action(self, action: argparse.Action) -> str:
        """
        Remove subcommand metavar tuple and fix metavar indentation.

        Override the _format_action method to remove the subcommand
        metavar tuple and fix the spacings between the option and its
        associated metavar.

        :param action: The action in which to be formatted.
        :type action: argparse.Action
        :return: super's _format_action. Will be formatted without the
            metavar tuple, as well as the correct leading indentation if
            the action is an argparse._SubParsersAction.
        :rtype: str
        """
        # Overrides the superclass _format_action method
        # Fix indentation for subclasses
        result: str = super()._format_action(action)
        if isinstance(action, argparse._SubParsersAction):
            # Return result with leading spaces removed, and
            # appropriate indentation added.
            return f"{'':{self._current_indent}}{result.lstrip()}"
        return result

    def _iter_indented_subactions(
        self,
        action: argparse.Action,
    ) -> Generator[argparse.Action, None, None]:
        """
        Fix leading indentation for subcommand names in help menu.

        Override the _iter_indented_subactions method to fix the leading
        indentation for subcommand names in the help menu.

        :param action: The action to be yielded from.
        :type action: argparse.Action
        :yield: Actions from a list returned by action._get_subactions.
        :rtype: Generator[argparse.Action, None, None]
        """
        # Overrides the superclass _iter_indented_subactions method
        # Fixes indentation on subcommand metavar
        if isinstance(action, argparse._SubParsersAction):
            try:
                # Get reference of subclass
                subactions: Callable[[], list[argparse.Action]] = action._get_subactions
            except AttributeError:
                # If an exception is found, do nothing
                pass
            else:
                # Yield from the actions list
                yield from subactions()
        else:
            # Yield from superclass' _iter_indented_subactions method
            yield from super()._iter_indented_subactions(action)


def _int_checking(user_input: str, upper_bound: int) -> int:
    """
    Return user_input as an integer if 0 < user_input < upper_bound.

    Cast user_input to an integer. If user_input is not an integer or is
    not 0 < user_input < upper_bound, then raise an
    argparse.ArgumentTypeError.

    :param user_int: The user's input as a string.
    :type user_int: str
    :param upper_bound: The maximum value that int(user_input) can be.
    :type upper_bound: int
    :raises argparse.ArgumentTypeError: Raised if user_input is not an
        integer or is not 0 < int(user_input) < upper_bound.
    :return: Return user_input as an integer.
    :rtype: int
    """
    with contextlib.suppress(ValueError):
        if 0 < (casted_int := int(user_input)) < upper_bound:
            return casted_int
    msg = f"Input '{user_input}' must be an integer between 1 and {upper_bound}."
    raise argparse.ArgumentTypeError(msg)


class WarMACParser(argparse.ArgumentParser):
    """
    Extend argparse.ArgumentParser to reimplement the error function.

    Extend argparse.ArgumentParser to reimplement the standard error
    function so it exits with status code 2, and prints to stderr.
    """

    def error(self, message: str) -> NoReturn:
        """
        Modify exit message for argparse.ArgumentError occurrences.

        Modify exit message for argparse.ArgumentError occurrences to
        print to sys.stderr and return an exit code of 2.

        :param message: The message provided by the standard
            argparse.ArgumentParser class.
        :type message: str
        :return: A value is never returned by this function.
        :rtype: NoReturn
        """
        self.exit(2, f"{self.usage}: error: {message}\n")


def _create_parser() -> WarMACParser:
    """
    Create the command-line parser for the program.

    Create an argparse.ArgumentParser object that includes global
    --help and --version options. Create subparsers for multiple
    subcommands to be used within the program.

    :return: The constructed ArgumentParser object.
    :rtype: WarMACParser
    """
    parser = WarMACParser(
        usage=f"{warmac_errors.PROG_NAME} <command> [options]",
        description=warmac_errors.DESCRIPTION,
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,  # first arg in CL, which is the file's name
            max_help_position=_DEFAULT_WIDTH,
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
        version=f"{warmac_errors.PROG_NAME} {warmac_errors.VERSION}",
    )

    # ======= Sub-Commands =======
    subparsers = parser.add_subparsers(dest="subparser", metavar="")

    # ------- Average -------
    avg_parser = subparsers.add_parser(
        "average",
        help="Calculate the average platinum price of an item.",
        description=(
            "Calculate the average platinum price of an item. Able to find the median,"
            " mean, mode, geometric mean, and harmonic mean of the specified item."
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,
            max_help_position=_DEFAULT_WIDTH,
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
        usage=(
            f"{warmac_errors.PROG_NAME} average [-s <stat>] [-p <platform>] [-t <days>]"
            " [-m | -r] [-b] item"
        ),
    )

    # Option characters used: s, p, t, m, r, b, v, h

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
            f"{_MAX_TIME_RANGE}]. (Default: {DEFAULT_TIME})"
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


def handle_input() -> argparse.Namespace:
    """
    Create argparse.ArgumentParser and parse arguments.

    Create argparse.ArgumentParser object, parse command-line arguments,
    and return the parsed arguments as an argparse.Namespace object.
    Exits early if only "warmac" is called.

    :return: The parsed command-line arguments.
    :rtype: argparse.Namespace
    """
    parser = _create_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()
