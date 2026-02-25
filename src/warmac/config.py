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

import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Literal

    AverageType = Literal["geometric", "mean", "median", "mode"]

# The default time to collect orders until
DEFAULT_TIME = 5
# The default number of digits to round to
DEFAULT_NDIGITS = 1
# The current version of WarMAC
VERSION = "0.0.5"

AVERAGE_FUNCTIONS: Mapping[AverageType, Callable[[Sequence[int]], float]] = {
    "geometric": statistics.geometric_mean,
    "mean": statistics.mean,
    "median": statistics.median,
    "mode": statistics.mode,
}
