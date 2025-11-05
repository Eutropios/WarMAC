"""
warmac.main
~~~~~~~~~~~

WarMAC — https://github.com/Eutropios/WarMAC
Copyright (C) 2024  Noah Jenner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------

Main logic of warmac.
"""  # noqa: D205, D400

from __future__ import annotations

import datetime
import sys
from typing import TYPE_CHECKING

from warmac import average, cli_parser, errors

if TYPE_CHECKING:
    from typing import Literal


SUBCMD_DISPATCH = {
    "average": average.process_data,
}


def fix_http_headers(
    http_headers: dict[str, str],
    platform: Literal["pc", "ps4", "xbox", "switch", "mobile"] = "pc",
    *,
    crossplay: bool = True,
) -> None:
    """
    Append the platform name and crossplay status to HTTP headers dict.

    Append the platform name and crossplay status to a dictionary
    containing HTTP headers.

    :param http_headers: HTTP headers dictionary.
    :param platform: Desired platform, defaults to "pc".
    :param crossplay: Crossplay status, defaults to True.
    """
    http_headers["Platform"] = platform
    http_headers["Crossplay"] = str(crossplay).lower()


def process_cli_command(args: list[str] | None) -> str:
    """
    Parse cli args, set up headers, and execute appropriate subcommand.

    Call :func:`cli_parser.handle_input` to create and parse a
    :class:`cli_parser.WarMACParser`, create http headers for the http
    request, and execute the function associated with the specified
    subcommand.

    :param args: Optional cli args used for testing.
    :return: The data returned from the subcommand handler.
    """
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
    }
    cli_args = cli_parser.handle_input(args)
    fix_http_headers(headers, cli_args.platform, crossplay=cli_args.crossplay)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return SUBCMD_DISPATCH[cli_args.subparser](cli_args, headers, current_time)


def main(args: list[str] | None = None) -> Literal[0, 1]:
    """
    Entry point for WarMAC.

    Orchestrate core logic and handle errors for WarMAC.

    :param args: Optional cli args used for testing.
    :return: 0 if execution is successful, 1 otherwise.
    """
    try:
        data = process_cli_command(args)
    except KeyError as err:
        raise errors.CommandError from err
    except errors.WarMACBaseError as err:
        sys.stderr.write(err.message)
        return 1
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
