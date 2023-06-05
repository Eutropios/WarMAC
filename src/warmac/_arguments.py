"""
warmac._arguments
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the argument parser for WarMac.
For information on the main program, please see main.py

Date of Creation: January 22, 2023
Date Last Modified: June 4, 2023
Version of Python required for module: >=3.9.0
"""  # noqa: D205,D400

from __future__ import annotations

import argparse as argp
import shutil
from statistics import harmonic_mean, mean, median, mode
from typing import Union

try:
    from src.warmac import _classdefs  # type: ignore
except ImportError:
    import _classdefs  # type: ignore


AVG_FUNCS: dict[str, function] = {  # noqa: F821
    "mean": mean,
    "median": median,
    "mode": mode,
    "harmonic": harmonic_mean,
}

_DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."
_HELP_MIN_WIDTH = 100
_PLATFORMS = ("pc", "ps4", "xbox", "switch")
_UPPER_TIME_BOUNDS = 750


class CustomHelpFormatter(argp.HelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: Union[int, None] = None,
    ) -> None:
        super().__init__(prog, indent_increment, max_help_position, width)

    def _format_action_invocation(self, action: argp.Action) -> str:
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ", ".join(action.option_strings) + " " + args_string


def _int_checking(inp: str, /) -> int:
    """
    Take string input and check if it's an integer greater than 0 and less than 750.

    :param inp: argument parser's time range value to be checked against
    :type inp: str
    :raises ArgumentTypeError: if inp is a string, or if inp <= 0, or
    if inp >= _UPPER_BOUNDS
    :return: returns inp if inp > 0 and if inp < _UPPER_BOUNDS
    :rtype: int
    """
    try:
        new_inp = int(inp)
    except ValueError:
        msg = "Input mismatch error. Please use an integer greater than 0."
        raise argp.ArgumentTypeError(msg) from None
    if new_inp <= 0 or new_inp >= _UPPER_TIME_BOUNDS:
        msg = "Invalid integer. Please use an integer greater than 0."
        raise argp.ArgumentTypeError(msg)
    return new_inp


def create_parser() -> argp.ArgumentParser:
    """
    Return ArgumentParser with the appropriate documentation and functionality.

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
    parser = argp.ArgumentParser(
        formatter_class=lambda prog: CustomHelpFormatter(
            prog=prog, max_help_position=width
        ),
        description=_DESCRIPTION,
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="help", help="Show this message and exit."
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show the program's version number and exit.",
        version="%(prog)s" f" {_classdefs.VERSION}",
    )

    # Optional Arguments
    parser.add_argument(
        "-a",
        "--avgtype",
        default="mean",
        type=lambda s: s.lower().strip(),
        choices=AVG_FUNCS,
        help=(
            "Specifies the type of average to return; Can be one of "
            f"[{', '.join(AVG_FUNCS)}]. (Default: mean)"
        ),
        metavar="<type>",
        dest="avg_type",
    )

    parser.add_argument(
        "-b",
        "--buyers",
        action="store_true",
        help=(
            "Take the average platinum price from buyer orders instead of "
            "seller orders."
        ),
        dest="use_buyers",
    )

    parser.add_argument(
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

    parser.add_argument(
        "-r",
        "--range",
        default=60,
        type=_int_checking,
        help=(
            "Specifies in days how old the orders can be. Must be in range [1, "
            f"{_UPPER_TIME_BOUNDS}]. (Default: 60)"
        ),
        metavar="<days>",
        dest="time_range",
    )

    # Positional Arguments
    parser.add_argument(
        "item",
        type=lambda s: s.strip(),
        help="the item to find the average of",
    )
    return parser
