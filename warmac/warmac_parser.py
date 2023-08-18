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
import shutil
import sys
from typing import TYPE_CHECKING, NoReturn, Union

from warmac import warmac_errors

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

AVG_FUNCS = ("median", "mean", "mode", "harmonic", "geometric")
DEFAULT_TIME = 15
_DEFAULT_WIDTH = min(34, shutil.get_terminal_size().columns - 2)
_MAX_TIME_RANGE = 60
_PLATFORMS = ("pc", "ps4", "xbox", "switch")


class CustomHelpFormat(argparse.RawDescriptionHelpFormatter):
    """
    Custom help formatter for argparse.ArgumentParser.

    Extends argparse.RawDescriptionHelpFormatter. Overrides
    _format_action, _format_action_invocation, and
    _iter_indented_subactions to remove the subcommand metavar tuple,
    remove duplicate option metavar, and correct over-indentation on the
    help menu respectively.
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
        :param max_help_position: How wide the space between each
            argument and its associated help text should be, defaults to
            24.
        :type max_help_position: int, optional
        :param width: The total width that the help screen is able to
            occupy in the terminal, defaults to None.
        :type width: Union[int, None], optional
        """
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Override the superclass _format_action_invocation method.

        Override the superclass' _format_action_invocation method to
        remove the duplicate metavar in the help display for options
        that have both a short form and long form.

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
        Override the superclass' _format_action method.

        Override the superclass' _format_action method to fix the
        leading indentation of subparsers on the help page.

        :param action: The action in which to be formatted.
        :type action: argparse.Action
        :return: super's _format_action, formatted with the correct
            leading indentation if the action is an
            argparse._SubParsersAction.
        :rtype: str
        """
        # Overrides the superclass _format_action method
        # *ix indentation for subclasses
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
        Override the superclass _iter_indented_subactions method.

        Override the superclass' _iter_indented_subactions method to
        yield from subactions if the action is an
        argparse._SupParsersAction.

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


def _int_checking(user_int: str, upper_bound: int) -> Union[int, None]:
    """
    Check if input is an integer and is within range.

    Cast input as an integer and raise an argparse.ArgumentTypeError if
    unable to. Raise an argparse.ArgumentTypeError if integer is not
    greater than 0 and less than upper_bounds.

    :param user_int: The user's input.
    :type user_int: str
    :param upper_bound: The maximum value that the user's input can be.
    :type upper_bound: int
    :raises ValueError: Is thrown if the input is not an integer. Is
        then caught within the function and is raised again as an
        argparse.ArgumentTypeError.
    :raises argparse.ArgumentTypeError: Is thrown if the input is not an
        integer, if the integer is less than 0, or if the integer is
        greater than upper_bounds.
    :return: None if the user's input is not an integer or if the user's
        input is not within range. Returns the user's input casted as an
        integer if it's within range.
    :rtype: Union[int, None]
    """
    try:
        casted_int = int(user_int)
    except ValueError:
        msg = f"Argument must be an integer greater than 0 and less than {upper_bound}."
        raise argparse.ArgumentTypeError(msg) from None
    if not (0 < casted_int <= upper_bound):
        msg = f"Argument must be greater than 0 and less than {upper_bound}."
        raise argparse.ArgumentTypeError(msg) from None
    return casted_int


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
        self.print_help(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def _create_parser() -> argparse.ArgumentParser:
    """
    Create the command-line parser for the program.

    Create the command-line parser using the built-in library argparse.
    Create an argparse.ArgumentParser object and add "help" and
    "version" options to it. Create subparsers for multiple subcommands
    to be used within the program.

    :return: The constructed ArgumentParser object.
    :rtype: argparse.ArgumentParser
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
    avg_parser: argparse.ArgumentParser = subparsers.add_parser(
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
    Create and perform checks on command-line arguments.

    Create argparse.ArgumentParser object, parse command-line arguments,
    and return the parsed arguments as an argparse.Namespace object.

    :return: The parsed command-line arguments.
    :rtype: argparse.Namespace
    """
    parser: argparse.ArgumentParser = _create_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()