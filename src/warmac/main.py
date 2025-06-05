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

from warmac import average, cli_parser

if TYPE_CHECKING:
    # import argparse
    from typing import Literal

SUBCMD_TO_FUNC = {
    "average": average.main,
}


def main(args: list[str] | None = None) -> Literal[0]:
    """
    Create a :data:`cli_parser.WarMACParser` and run associated command.

    Call :func:`cli_parser.handle_input` to create and parse a
    :class:`cli_parser.WarMACParser`. Arguments are then used in
    the script's execution.

    :return: Return 0 if everything returns successfully.
    """
    cli_args = cli_parser.handle_input(args)
    output_val = SUBCMD_TO_FUNC[cli_args.subparser](cli_args)
    print(output_val)
    return 0


if __name__ == "__main__":
    sys.exit(main())
