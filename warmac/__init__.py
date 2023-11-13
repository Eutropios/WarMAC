"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Warframe Market Average Calculator (WarMAC) 0.0.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

Retrieves the sell price from all orders of a given item from
https://warframe.market for a specific platform, then finds the average
price in platinum of the orders.

Date of Creation: January 22, 2023
External packages required: urllib3
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import sys
from typing import Callable, Dict, Literal

from urllib3 import exceptions

from warmac import warmac_average, warmac_errors, warmac_parser

__all__ = [
    "warmac_average",
    "warmac_errors",
    "warmac_parser",
]

#: A dictionary of all possible subcommands
SUBCMD_TO_FUNC: Dict[str, Callable[[argparse.Namespace], None]] = {
    "average": warmac_average.average,
}


def subcommand_select(args: argparse.Namespace) -> None:
    """
    Select which function to use based on ``args.subparser`` field.

    Use a try block and a dictionary to execute the appropriate function
    corresponding to the field ``args.subparser``.

    :param args: The :py:class:`argparse.Namespace` containing the
        user-supplied command line information.
    :raises SubcommandError: An error indicating that the
        desired subcommand does not exist within the
        :py:data:`.SUBCMD_TO_FUNC` dictionary.
    """
    try:
        SUBCMD_TO_FUNC[args.subparser](args)
    except KeyError as err:
        raise warmac_errors.SubcommandError from err
    except warmac_errors.WarMACBaseError as e:
        print(e)
    except exceptions.MaxRetryError:
        print(
            "You're not connected to the internet. Please check your internet "
            "connection and try again.",
        )
    except exceptions.TimeoutError:
        print("The connection timed out. Please try again later.")
    except exceptions.HTTPError:
        print("Unknown connection error.")


def console_main() -> Literal[0]:
    """
    Create a :py:data:`warmac_parser.WarMACParser` and run associated
    subcommand.

    Call :py:func:`warmac_parser.handle_input` to create and parse a
    :py:class:`warmac_parser.WarMACParser`. Arguments are then used in
    the script's execution, beginning by calling
    :py:func:`.subcommand_select` with the parsed arguments.
    :return: Return 0 if everything returns successfully.
    """  # noqa: D205
    subcommand_select(warmac_parser.handle_input())
    return 0


if __name__ == "__main__":
    sys.exit(console_main())
