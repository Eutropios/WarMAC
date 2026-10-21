"""Main logic of warmac.

-----------------------------------------------------------------------

WarMAC — https://github.com/Eutropios/WarMAC Copyright (C) 2024  Noah
Jenner

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import datetime as dt
import sys
from typing import TYPE_CHECKING

from warmac import average, cli_parser, errors

if TYPE_CHECKING:
    from collections.abc import MutableMapping, Sequence
    from typing import Literal

# A dictionary of all commands that can be executed by the user.
SUBCMD_DISPATCH = {
    "average": average.process_data,
}


def fix_http_headers(
    http_headers: MutableMapping[str, str],
    platform: Literal["pc", "ps4", "xbox", "switch", "mobile"] = "pc",
    *,
    crossplay: bool = True,
) -> None:
    """Append platform name and crossplay status to HTTP headers dict.

    Append the platform name and crossplay status to a dictionary
    containing HTTP headers.

    Args:
        http_headers: HTTP headers dictionary.
        platform: Desired platform, defaults to "pc".
        crossplay: Crossplay status, defaults to True.
    """
    http_headers["Platform"] = platform
    http_headers["Crossplay"] = str(crossplay).lower()


def process_cli_command(args: Sequence[str] | None) -> str:
    """Process the command line arguments and execute command.

    Call cli_parser.handle_input to create and parse a
    cli_parser.WarMACParser, create http headers for the http request,
    and execute the function associated with the specified subcommand.

    Args:
        args: Optional cli args used for testing.

    Returns:
        The data returned from the subcommand handler.

    Raises:
        errors.CommandError: Raised if the subparser field of
            argparse.Namespace does not exist in main.SUBCMD_DISPATCH.
    """
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
    }
    cli_args = cli_parser.handle_input(args)
    fix_http_headers(headers, cli_args.platform, crossplay=cli_args.crossplay)
    current_time = dt.datetime.now(dt.UTC)
    try:
        subcmd = SUBCMD_DISPATCH[cli_args.subparser](cli_args, headers, current_time)
    except KeyError as err:
        raise errors.CommandError from err
    return subcmd


def main(args: Sequence[str] | None = None) -> Literal[0, 2]:
    """Entry point for WarMAC.

    Orchestrate core logic and handle errors for WarMAC.

    Args:
        args: Optional cli args used for testing.

    Returns:
        0 if execution is successful, 2 if an error is encountered.
    """
    try:
        data = process_cli_command(args)
    except errors.WarMACBaseError as err:
        sys.stderr.write(err.message)
        return 2
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
