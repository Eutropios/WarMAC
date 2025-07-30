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

http_headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
}


def fix_http_headers(
    http_headers: dict[str, str],
    platform: Literal["pc", "ps4", "xbox", "switch", "mobile"] = "pc",
    *,
    crossplay: bool = True,
) -> None:
    """
    Append the platform name and crossplay status to HTTP headers dict.

    :param http_headers: HTTP headers dictionary.
    :param platform: Desired platform, defaults to "pc".
    :param crossplay: Crossplay status, defaults to True.
    """
    http_headers["Platform"] = platform
    http_headers["Crossplay"] = str(crossplay).lower()


def main(args: list[str] | None = None) -> Literal[0, 1]:
    """
    Create a :data:`cli_parser.WarMACParser` and run associated command.

    Call :func:`cli_parser.handle_input` to create and parse a
    :class:`cli_parser.WarMACParser`. Arguments are then used in
    the script's execution.

    :param args: Optional cli args. Should be used for testing.
    :return: Return 0 if everything returns successfully.
    """
    try:
        cli_args = cli_parser.handle_input(args)
        fix_http_headers(http_headers, cli_args.platform, crossplay=cli_args.crossplay)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        # When Python 3.10 EOL, change to:
        # current_time = datetime.datetime.now(datetime.UTC)
        data = SUBCMD_DISPATCH[cli_args.subparser](cli_args, http_headers, current_time)
        print(data)
    except KeyError as err:
        raise errors.CommandError from err
    except errors.WarMACBaseError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
