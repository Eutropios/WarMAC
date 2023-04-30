"""
warmac._arguments
~~~~~~~~~~~~~~~~~
File that contains argument handling and error handling
"""

import shutil
from argparse import (
    ArgumentParser as ArgP,
    RawDescriptionHelpFormatter as DescHelpFormat,
    ArgumentDefaultsHelpFormatter as DefaultHelpFormat,
    RawTextHelpFormatter as RawHelpFormat
)

PLATFORMS = ("pc", "ps4", "xbox", "switch")
HELP_MIN_WIDTH = 90

class SpecialParser(DefaultHelpFormat, RawHelpFormat, DescHelpFormat):
    """
    Extends argparse.ArgumentDefaultsHelpFormatter and argparse.RawTextHelpFormatter
    """
    pass

class DatabaseError(Exception):
    def __init__(self, message="Database Error."):
        self.message = message
        super().__init__(self.message)

def create_parser() -> ArgP:
    """Returns ArgumentParser with the appropriate documentation and
    functionality

    :return: ArgumentParser with appropriate documentation and functionality
    :rtype: argparse.ArgumentParser
    """
    width = min(HELP_MIN_WIDTH, shutil.get_terminal_size().columns - 2)
    parser = ArgP(description="A program to fetch the average cost of an item in Warframe.",
                  formatter_class=lambda prog: SpecialParser(prog, max_help_position=width))

    # Optional Arguments
    parser.add_argument('-p', "--platform", default="pc", type=lambda s: s.lower().strip(),
                        choices=PLATFORMS, metavar="", help="Specifies which platform to fetch"
                        " listings for; can be either\nps4, xbox, pc, or switch")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the average price of"
                        " the item, alongside a short\nmessage for the user.", dest="verbose")
    parser.add_argument("-e", "--extra-info", action="store_true", help="Prints the highest and"
                        " lowest prices in the order list, as well\nas the number of orders that"
                        " were fetched.", dest="extra")
    # parser.add_argument("-r", "--range", default=60, type=int, help="", metavar="\b", dest="time_range")
    # parser.add_argument("--no-colour", action="store_true", help="No colour mode. Removes colour "
    #                    "from script output; Ideal for\nterminals that are incompatible with ANSI"
    #                    " colouring.", dest="no_colour")

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
