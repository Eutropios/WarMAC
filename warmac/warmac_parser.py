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

#: The default time to collect orders until
DEFAULT_TIME = 10
#: The statistic types that the average command can use
_AVG_FUNCS = ("median", "mean", "mode", "harmonic", "geometric")
#: The description of the program
_DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."
#: The maximum time range that the average command can pull from
_MAX_TIME_RANGE = 60
#: The platforms that the user can choose from
_PLATFORMS = ("pc", "ps4", "xbox", "switch")
#: The name of the program.
_PROG_NAME = "warmac"
#: The current version of WarMAC
_VERSION = "0.0.5"


class CustomHelpFormat(argparse.RawDescriptionHelpFormatter):
    """
    Custom help formatter for :py:class:`warmac_parser.WarMACParser`.

    Extend :py:class:`argparse.RawDescriptionHelpFormatter` to
    reimplement a few methods. Reimplementations include removing the
    command metavar tuples, removing the duplicate option metavars,
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
        have both a short-form and a long-form argument.

        :param action: The action in which to be formatted.
        :return: The appropriately formatted string.
        """
        # Return super's invocation option_string is None or nargs is 0
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        # Get the default metavar for optionals
        default = self._get_default_metavar_for_optional(action)
        # Return the option strings joined with only one metavar
        return (
            f"{', '.join(action.option_strings)} {self._format_args(action, default)}"
        )

    def _format_action(self, action: argparse.Action) -> str:
        """
        Remove command metavar tuple and fix metavar indentation.

        Override the ``HelpFormatter._format_action``
        method to remove the command metavar tuple and fix the
        spacings between the option and its associated metavar.

        :param action: The action in which to be formatted.
        :return: ``HelpFormatter._format_action(action)``. If the action
            is a ``_SubParsersAction``, the metavar tuple will be
            excluded, and the leading indentation will be corrected.
        """
        # Fix indentation for subclasses
        result = super()._format_action(action)
        return (
            f"{'':{self._current_indent}}{result.lstrip()}"
            if isinstance(action, argparse._SubParsersAction)
            else result
        )

    def _iter_indented_subactions(
        self,
        action: argparse.Action,
    ) -> Generator[argparse.Action, None, None]:
        """
        Fix leading indentation for command names in the help menu.

        Override the ``HelpFormatter._iter_indented_subactions``
        method to fix the leading indentation for command names in
        the help menu.

        :param action: The action to be yielded from.
        :yield: Actions from a list returned by
            ``action._get_subactions``.
        """
        # Overrides the superclass _iter_indented_subactions method
        # Fixes indentation on command metavar
        if isinstance(action, argparse._SubParsersAction):
            with contextlib.suppress(AttributeError):
                # Yield from actions list if action has _get_subactions
                yield from action._get_subactions()
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
    msg = f'Input "{usr_inp}" must be an integer between 1 and {max_val}.'
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
        occurrences to print to stderr, and return an exit code of 2.

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
    commands to be used within the program.

    :return: The constructed :py:class:`.WarMACParser` object.
    """
    help_min_width = 34  # min width that help text should take up in usage
    # Min value of help_min_width and terminal's width
    default_width = min(help_min_width, shutil.get_terminal_size().columns - 2)
    parser = WarMACParser(
        usage=f"{_PROG_NAME} <command> [options]",
        description=_DESCRIPTION,
        epilog=(
            "More help can be found at: "
            "https://warmac.readthedocs.io/en/latest/usage/warmac.html"
        ),
        formatter_class=lambda prog: CustomHelpFormat(
            prog=prog,  # first arg in CL, which is the file's name
            max_help_position=default_width,
        ),
        add_help=False,  # don't add default help msg
    )
    parser._positionals.title = "commands"  # changing positional header

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
            max_help_position=default_width,
            # prog refers to the first argument passed in the command
            # line, which is the name of the file in this case.
        ),
        add_help=False,
        usage=(
            f"{_PROG_NAME} average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r]"
            " [-b] [-v] item"
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
            f"({', '.join(_AVG_FUNCS)}). (Default: median)"
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
            "Which platform to fetch the item's orders for. Must be one of "
            f"({', '.join(_PLATFORMS)}). (Default: pc)"
        ),
        metavar="<platform>",
    )

    avg_parser.add_argument(
        "-t",
        "--timerange",
        default=DEFAULT_TIME,
        type=lambda x: _int_checking(x, _MAX_TIME_RANGE),
        help=(
            "Number of days to consider for calculating the average. Value given "
            "indicates how far back to start the statistic's calculation. Must be in "
            f"range [1, {_MAX_TIME_RANGE}]. (Default: {DEFAULT_TIME})"
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
            "Calculate the price statistic of the mod/arcane at its maximum rank "
            "instead of when it is unranked. Cannot be used together with the --radiant"
            " option."
        ),
        dest="maxrank",
    )

    max_or_rad.add_argument(
        "-r",
        "--radiant",
        action="store_true",
        help=(
            "Calculate the price statistic of the relic at a radiant refinement instead"
            " of at an intact refinement. Cannot be used together with the --maxrank "
            "option."
        ),
        dest="radiant",
    )

    avg_parser.add_argument(
        "-b",
        "--buyers",
        action="store_true",
        help=(
            "Calculate the price statistic of the item based on orders from buyers "
            "instead of orders from sellers."
        ),
        dest="use_buyers",
    )

    avg_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=(
            "Print additional market information about the requested item, along with "
            "the specified parameters."
        ),
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
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()
