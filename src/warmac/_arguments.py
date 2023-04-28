"""
Files that contains argument handling and error handling
"""

import shutil
from argparse import ArgumentParser as AP, ArgumentDefaultsHelpFormatter as DefaultHelpFormat
from argparse import RawTextHelpFormatter as RawHelpFormat

PLATFORMS = ("pc", "ps4", "xbox", "switch")
# PARSER_DESCRIPTION

class SpecialParser(DefaultHelpFormat, RawHelpFormat):
    """
    Extends argparse.ArgumentDefaultsHelpFormatter and argparse.RawTextHelpFormatter
    """
    pass

def create_parser() -> AP:
    """Returns ArgumentParser withthe appropriate documentation and
    functionality

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(90, shutil.get_terminal_size().columns - 2)
    parser = AP(description="A program to fetch the average cost of an item in Warframe.",
                formatter_class=lambda prog: SpecialParser(prog, max_help_position=width))

    # Optional Arguments
    parser.add_argument('-p', "--platform", default="pc", type=lambda s: s.lower().strip(),
                        choices=PLATFORMS, metavar="", help="Specifies which platform to fetch"
                        " listings for; can be either\nps4, xbox, pc, or switch")
    parser.add_argument("-l", "-v", "--listings", "--verbose", action="store_true", help="Listing"
                        " mode. Shows each listing that is being used to\ncalculate the average "
                        "price; Highest level of verbosity.", dest="listings")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-m", "--minimal", action="store_true", help="Minimal ouptut mode. Removes"
                        " execessive text and instead only shows\nthe average price; No colour is "
                        "present in the output.", dest="minimal")
    group1.add_argument("--no-colour", action="store_true", help="No colour mode. Removes colour "
                        "from script output; Ideal for\nterminals that are incompatible with ANSI"
                        " colouring.", dest="no_colour")

    # Positional Arguments
    parser.add_argument("item", type=lambda s: s.lower().strip(), help="the item to search for")
    return parser

def err_handling(err_code: int):
    """Function that handles self-generated error codes within the program

    :param err_code: integer corresponding to a partciular error code.
    :type err_code: int
    """

    match err_code:
        case 1:
            print("You're not connected to the internet. Please check your internet connection and"
                  " try again.")
        case 2:
            print("There were no listings of this item within the past 2 months found.")
        case 3:
            print("This item does not exist. Please check your spelling, and remember to use "
                  "parenthesis in the command line if the item is multiple words.")
        case 4:
            print("Database error. Please open a new issue on the Github/Gitlab page (link in "
                  "README.rst file).")
        case _:
            print("Unknown error, writing to errorLog.txt file. Please open a new issue on the "
                  "Github/Gitlab page (link in README.rst file).")
