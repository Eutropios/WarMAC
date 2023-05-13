"""
warmac._arguments
~~~~~~~~~~~~~~~~~
File that contains argument handling and error handling.
""" # noqa

import shutil
from argparse import ArgumentParser as ArgParser
from argparse import ArgumentTypeError as ArgTypeError
from argparse import RawDescriptionHelpFormatter as DescHelpFormat
from argparse import RawTextHelpFormatter as RawHelpFormat
from statistics import geometric_mean as geometric
from statistics import harmonic_mean as harmonic
from statistics import mean, median, mode
from src.warmac import _VERSION

_AVG_FUNCTIONS = {
    "mean": mean,
    "median": median,
    "mode": mode,
    "harmonic": harmonic,
    "geometric": geometric,
}
_HELP_MIN_WIDTH = 100
_PLATFORMS = ("pc", "ps4", "xbox", "switch")
_UPPER_BOUNDS = 750

class _SpecialParser(RawHelpFormat, DescHelpFormat):
    """Extends argparse.RawDescriptionHelpFormatter and argparse.RawTextHelpFormatter."""

def _int_checking(inp: int | str) -> int:
    """
    Take string or integer and check if it's greater than 0 and less than 750.

    :param inp: argument parser's time range value to be checked against
    :type inp: int | str
    :raises ArgTypeError: if input is a string, or if inp <= 0, or if input >= _UPPER_BOUNDS
    :return: returns inp if inp > 0 and if inp < _UPPER_BOUNDS
    :rtype: int
    """
    try:
        inp = int(inp)
    except ValueError:
        msg = "Input mismatch error. Please use an integer greater than 0."
        raise ArgTypeError(msg) from None
    if inp <= 0 or inp >= _UPPER_BOUNDS:
        msg = "Invalid integer. Please use an integer greater than 0."
        raise ArgTypeError(msg)
    return inp

def _create_parser() -> ArgParser:
    """
    Return ArgumentParser with the appropriate documentation and functionality.

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(_HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
    parser = ArgParser(description="A program to fetch the average cost of an item in Warframe.",
                       formatter_class=lambda prog: _SpecialParser(prog, max_help_position=width),
                       add_help=False)

    parser.add_argument("-h", "--help", action="help", help="Show this message and exit.")
    parser.add_argument("--version", action="version", help="Show the program's version number"
                        " and exit.", version="%(prog)s" f" {_VERSION}")

    # Optional Arguments
    parser.add_argument("-a", "--avg_type", default="mean", type=lambda s: s.lower().strip(),
                        choices=_AVG_FUNCTIONS, metavar="", help="Specifies the type of average to"
                        f" return; Can be one of {', '.join(_AVG_FUNCTIONS)}. (Default: mean)")
    parser.add_argument("-b", "--buyers", action="store_true", help="Take the average platinum"
                        " price from buyer listings instead of seller listings.")
    parser.add_argument("-e", "--extra-info", action="store_true", help="Prints the highest and"
                        " lowest prices in the order list, as well as the number of orders that"
                        " were fetched.", dest="extra")
    parser.add_argument("-p", "--platform", default="pc", type=lambda s: s.lower().strip(),
                        choices=_PLATFORMS, metavar="", help="Specifies which platform to fetch"
                        f" listings for; Can be one of {', '.join(_PLATFORMS)}. (Default: pc)")
    parser.add_argument("-r", "--range", default=60, type=_int_checking, help="Specifies in days"
                        " how old the retrieved listings can be. Must be greater than 0 and less"
                        " than 750. (Default: 60)", metavar="", dest="time_r")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the average price of"
                        " the item, alongside a short message for the user.", dest="verbose")

    # Positional Arguments
    parser.add_argument("item", type=lambda s: s.lower().strip(), help="the item to search for")
    return parser
