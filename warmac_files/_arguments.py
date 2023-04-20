"""
Files that contains argument handling and error handling
"""

from argparse import ArgumentParser as AP, ArgumentDefaultsHelpFormatter as DefHelpFormat
from argparse import RawTextHelpFormatter as RawHelpFormat

PLATFORMS = ("pc", "ps4", "xbox", "switch")

class SpecialParser(DefHelpFormat, RawHelpFormat):
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
    parser = AP(description="A program to fetch the average cost of an item in Warframe.",
                formatter_class=SpecialParser)

    # Optional Arguments
    parser.add_argument('-p', "--platform", default="pc", type=str.lower, choices=PLATFORMS,
                        metavar="", help="specifies which platform to fetch listings for; can be"
                        "\neither ps4, xbox, pc, or switch")
    parser.add_argument("-l", "--list", action="store_true", help="Listing mode. Shows "
                        "each listing that is being used to\ncalculate the average price.")
    parser.add_argument("--no-colour", action="store_true", help="No colour mode. Removes colour "
                        "from script output; Ideal for script command-line piping or terminals "
                        "incompatible with ANSI colouring.", dest="no_colour")

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
                  "parenthensis in the command line if the item is multiple words.")
        case 4:
            print("Database error. Please open a new issue on the Github/Gitlab page (link in "
                  "README.rst file)")
        case _:
            print("Unknwon error, writing to errorLog.txt file.")
