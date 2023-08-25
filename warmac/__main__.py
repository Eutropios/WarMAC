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

import sys
from typing import TYPE_CHECKING, Callable, Dict, Literal

from urllib3 import exceptions

from warmac import warmac_average, warmac_errors, warmac_parser

if TYPE_CHECKING:
    from argparse import Namespace

_SUBCMD_TO_FUNC: Dict[str, Callable[[Namespace], None]] = {
    "average": warmac_average.average,
}


def subcommand_select(args: Namespace, /) -> None:
    """
    Select which function to use based on args.subparser field.

    Use try block and a dictionary to execute the appropriate function
    corresponding to the field args.subparser.

    :param args: The argparse.Namespace containing the user-supplied
        command line information.
    :type args: Namespace
    :raises SubcommandError: An error indicating that the desired
        subcommand does not exist within the _SUBCMD_TO_FUNC dictionary.
    """
    try:
        _SUBCMD_TO_FUNC[args.subparser](args)
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
    Call _parser.handle_input and run subcommand_select with args.

    Call _parser.handle_input to acquire the argparse.Namespace object
    containing the command-line arguments passed in the script's
    execution. Call subcommand_select with argparse.Namespace as args.

    :return: Return 0 if everything returns successfully.
    :rtype: Literal[0]
    """
    args: Namespace = warmac_parser.handle_input()
    subcommand_select(args)
    return 0


if __name__ == "__main__":
    sys.exit(console_main())
