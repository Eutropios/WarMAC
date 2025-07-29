"""
warmac.config
~~~~~~~~~~~~~~

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

Global variables and constants.
"""  # noqa: D205, D400

from __future__ import annotations

import datetime
import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Literal

    AverageKind = Literal["geometric", "mean", "median", "mode"]

# The default time to collect orders until
DEFAULT_TIME = 10
# The default number of digits to round to
DEFAULT_NDIGITS = 1
# The current version of WarMAC
VERSION = "0.0.5"

# Convert to a match case when 3.9 EOL. Default case raises error
AVG_FUNCS: Mapping[AverageKind, Callable[[Sequence[int]], float]] = {
    "geometric": statistics.geometric_mean,
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
}

#: An ISO-8601 timestamp of the current time retrieved on execution.
CURR_TIME = datetime.datetime.now(datetime.timezone.utc)
# When Python 3.10 EOL, change to:
# CURR_TIME = datetime.datetime.now(datetime.UTC)
