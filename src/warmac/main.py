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

import sys
from typing import TYPE_CHECKING

from warmac import average, cli_parser, config, errors

if TYPE_CHECKING:
    import argparse
    from typing import Literal


SUBCMD_TO_FUNC = {
    "average": average.process_data,
}

http_headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
}


def fix_http_headers(
    http_headers: dict[str, str] = http_headers,
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


def detailed_output(
    stat: float, plat_list: list[int], args: argparse.Namespace
) -> None:
    """
    Display the calculated statistic along with additional information.

    Display the calculated statistic, along with the statistic used, the
    timerange of the request, the maximum and minimum prices of the
    orders, and the total number of orders that match the search
    criteria. If ``args.porcelain` is True, separate the fields with a
    single colon.

    :param stat: Statistic of the item that was found.
    :param plat_list: List of prices of the item.
    :param args: User-given command line arguments. Must have
        the fields ``statistic``, ``item``, ``porcelain``, and
        ``timerange``.
    """
    # {value:{width}.{precision}}
    statistic = config.AVG_FUNCS[args.statistic].__name__.replace("_", " ").title()
    fixed_item_name = args.item.title().replace("_", " ").replace(" And ", " & ")
    max_list = max(plat_list)
    min_list = min(plat_list)
    num_orders = len(plat_list)
    if args.porcelain:
        print(
            f"{fixed_item_name}:{statistic}:{args.timerange}:{stat}:{min_list}:"
            f"{max_list}:{num_orders}"
        )
    else:
        space_after_label = 23
        print(f"{'Item:':{space_after_label}}{fixed_item_name}")
        print(f"{'Statistic Found:':{space_after_label}}{statistic}")
        print(f"{'Time Range Used:':{space_after_label}}{args.timerange} days")
        print(f"{f'{statistic} Price:':{space_after_label}}{stat} platinum")
        print(f"{'Max Price:':{space_after_label}}{max_list:.0f} platinum")
        print(f"{'Min Price:':{space_after_label}}{min_list:.0f} platinum")
        print(f"{'Number of Orders:':{space_after_label}}{num_orders}")


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
        data = SUBCMD_TO_FUNC[cli_args.subparser](cli_args, http_headers)
        detailed_output(data["stat"], data["plat_list"], cli_args)
    except KeyError as err:
        raise errors.CommandError from err
    except errors.WarMACBaseError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
