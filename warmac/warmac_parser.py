"""
warmac.warmac_parser
~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the argument parser for WarMAC.
For information on the main program, please see __init__.py

Date of Creation: June 7, 2023
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import contextlib
import shutil
import sys
from typing import Generator, NoReturn, Union

#: The statistic types that the average command can use
_AVG_FUNCS = ("median", "mean", "mode", "harmonic", "geometric")
#: The default time to collect orders until
DEFAULT_TIME = 10
#: The description of the program
_DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."
#: The minimum width that the help text should take up in the CLI
_HELP_MIN_WIDTH = 34
#: Minimum of the minimum help width and the terminal width
_DEFAULT_WIDTH = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
#: The maximum time range that the average command can pull from
_MAX_TIME_RANGE = 60
#: The platforms that the user can choose from
_PLATFORMS = ("pc", "ps4", "xbox", "switch")
#: The name of the program.
_PROG_NAME = "warmac"
#: The current version of WarMAC
_VERSION = "0.0.4"


class CustomHelpFormat(argparse.RawDescriptionHelpFormatter):
    """
    Custom help formatter for :py:class:`warmac_parser.WarMACParser`.

    Extend :py:class:`argparse.RawDescriptionHelpFormatter` to
    reimplement a few methods. Reimplementations include removing the
    subcommand metavar tuples, removing the duplicate option metavars,
    and correcting the over-indentation on the help menu.
    """

    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: Union[int, None] = None,
    ) -> None:
        """
        Construct a :py:class:`.CustomHelpFormat` object.

        :param prog: The name of the program.
        :param indent_increment: How much space should come before the
            options on the help screen, defaults to 2.
        :param max_help_position: The width between ``indent_increment``
            and the help text, defaults to 24.
        :param width: The maximum width that the help screen is able to
            occupy in the terminal, defaults to None.
        """
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Remove duplicate metavar for options with short and long form.

        Override the ``HelpFormatter._format_action_invocation``
        method to remove the duplicate help metavar for options that
        have both a short form and long form argument.

        :param action: The action in which to be formatted.
        :return: The appropriately formatted string.
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

        Override the ``HelpFormatter._format_action``
        method to remove the subcommand metavar tuple and fix the
        spacings between the option and its associated metavar.

        :param action: The action in which to be formatted.
        :return: ``HelpFormatter._format_action(action)``.
            Will be formatted without the metavar tuple, as well as the
            correct leading indentation if the action is an
            ``_SubParsersAction``.
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
        self,  # noqa: PLR6301
        action: argparse.Action,
    ) -> Generator[argparse.Action, None, None]:
        """
        Fix leading indentation for subcommand names in help menu.

        Override the ``HelpFormatter._iter_indented_subactions``
        method to fix the leading indentation for subcommand names in
        the help menu.

        :param action: The action to be yielded from.
        :yield: Actions from a list returned by
            ``action._get_subactions``.
        """
        # Overrides the superclass _iter_indented_subactions method
        # Fixes indentation on subcommand metavar
        if isinstance(action, argparse._SubParsersAction):
            try:
                # Get reference of subclass
                subactions = action._get_subactions
            except AttributeError:
                # If an exception is found, do nothing
                pass
            else:
                # Yield from the actions list
                yield from subactions()
        else:
            # Yield from superclass' _iter_indented_subactions method
            yield from super()._iter_indented_subactions(action)


def _int_checking(usr_inp: str, max_val: int) -> int:
    """
    Return ``usr_inp`` as an integer if ``0 < usr_inp < max_val``.

    Cast ``usr_inp`` to an integer. If ``usr_inp`` is not an integer or
    is not ``0 < usr_inp < max_val``, then raise an
    :py:exc:`argparse.ArgumentTypeError`.

    :param usr_inp: The user's input as a string.
    :param max_val: The maximum value that ``int(usr_inp)`` can be.
    :raises argparse.ArgumentTypeError: Raised if ``usr_inp`` is not an
        integer or is not ``0 < int(usr_inp) < max_val``.
    :return: Return ``usr_inp`` as an integer.
    """
    with contextlib.suppress(ValueError):
        if 0 < (casted_int := int(usr_inp)) < max_val:
            return casted_int
    msg = f"Input '{usr_inp}' must be an integer between 1 and {max_val}."
    raise argparse.ArgumentTypeError(msg)


class WarMACParser(argparse.ArgumentParser):
    """
    Extend :py:class:`argparse.ArgumentParser` to reimplement the error
    method.

    Extend :py:class:`argparse.ArgumentParser` to reimplement the error
    method so it exits with status code 2, and prints to stderr.
    """  # noqa: D205

    def error(self, message: str) -> NoReturn:
        """
        Modify exit message for :py:class:`argparse.ArgumentError`.

        Modify exit message for :py:class:`argparse.ArgumentError`
        occurrences to print to stderr, and return an
        exit code of 2.

        :param message: The message provided by the standard
            :py:class:`argparse.ArgumentParser` class.
        :return: A value is never returned by this function.
        """
        self.exit(2, f"{self.usage}: error: {message}\n")


def _create_parser() -> WarMACParser:
    """
    Create the command-line parser for the program.

    Create a :py:class:`.WarMACParser` object that includes global
    --help and --version options. Create subparsers for multiple
    subcommands to be used within the program.

    :return: The constructed :py:class:`.WarMACParser` object.
    """
    parser = WarMACParser(
        usage=f"{_PROG_NAME} <command> [options]",
        description=_DESCRIPTION,
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
        version=f"{_PROG_NAME} {_VERSION}",
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
            f"{_PROG_NAME} average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r]"
            " [-b] item"
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
        choices=_AVG_FUNCS,
        help=(
            "Specifies which statistic to return; Can be one of "
            f"[{', '.join(_AVG_FUNCS)}]. (Default: median)"
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
    Create a :py:class:`.WarMACParser` and parse arguments.

    Create :py:class:`.WarMACParser` object, parse command-line
    arguments, and return the parsed arguments as an
    :py:class:`argparse.Namespace` object. Exits early if only "warmac"
    is called.

    :return: The parsed command-line arguments.
    """
    parser = _create_parser()
    parsed_args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parsed_args
