"""
warmac._arguments
~~~~~~~~~~~~~~~~~
File that contains argument handling and error handling.
""" # noqa

import shutil
from argparse import (
    ArgumentParser as ArgP,
    ArgumentTypeError as ArgTypeError,
    RawDescriptionHelpFormatter as DescHelpFormat,
    RawTextHelpFormatter as RawHelpFormat,
)
from src.warmac import VERSION

PLATFORMS = ("pc", "ps4", "xbox", "switch")
AVG_MODES = ("mean", "median", "mode", "harmonic")
HELP_MIN_WIDTH = 100


class SpecialParser(RawHelpFormat, DescHelpFormat):
    """Extends argparse.RawDescriptionHelpFormatter and argparse.RawTextHelpFormatter."""

    pass


def int_checking(inp: int | str) -> int:
    """Take string or integer and check if it's less than or equal to 0.

    :param inp: input integer
    :type inp: int
    :raises ArgumentTypeError: throw exception if inp <= 0
    :return: returns inp if inp > 0
    :rtype: int
    """
    try:
        inp = int(inp)
    except ValueError:
        raise ArgTypeError("Input mismatch error. Please use an integer greater than 0.") from None
    if inp <= 0:
        raise ArgTypeError("Invalid integer. Please use an integer greater than 0.")
    return inp


def create_parser() -> ArgP:
    """Return ArgumentParser with the appropriate documentation and functionality.

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
    parser = ArgP(description="A program to fetch the average cost of an item in Warframe.",
                  formatter_class=lambda prog: SpecialParser(prog, max_help_position=width),
                  add_help=False)

    parser.add_argument("-h", "--help", action="help", help="Show this message and exit.")
    parser.add_argument("--version", action="version", help="Show the program's version number"
                        " and exit.", version="%(prog)s" f" {VERSION}")

    # Optional Arguments
    parser.add_argument("-a", "--avg_type", default="mean", type=lambda s: s.lower().strip(),
                        choices=AVG_MODES, metavar="", help="Specifies the type of average to"
                        f" return; Can be one of {', '.join(AVG_MODES)}. (Default: mean)",
                        dest="avg_type")
    parser.add_argument("-e", "--extra-info", action="store_true", help="Prints the highest and"
                        " lowest prices in the order list, as well as the number of orders that"
                        " were fetched.", dest="extra")
    parser.add_argument("-p", "--platform", default="pc", type=lambda s: s.lower().strip(),
                        choices=PLATFORMS, metavar="", help="Specifies which platform to fetch"
                        f" listings for; Can be one of {', '.join(PLATFORMS)}. (Default: pc)")
    parser.add_argument("-r", "--range", default=60, type=int_checking, help="Specifies in days"
                        " the oldest a listing can be in order to be added to the calculation. Must"
                        " be greater than 0 and less than 750. (Default: 60)", metavar="",
                        dest="time_r")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the average price of"
                        " the item, alongside a short message for the user.", dest="verbose")

    # Positional Arguments
    parser.add_argument("item", type=lambda s: s.lower().strip(), help="the item to search for")
    return parser
