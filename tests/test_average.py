"""
tests.test_average
~~~~~~~~~~~~~~~~~

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

Test file for average.py
"""  # noqa: D205, D400

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

# from unittest.mock import MagicMock, Mock
import pytest

from warmac import average, cli_parser, errors

if TYPE_CHECKING:
    AverageKind = average.AverageKind


class TestCalcAvg:
    # test if plat_list is empty that an error is thrown
    # test that if statistic param not in AVG_FUNCS
    # test if decimals is not passed, that result rounded to 1 decimal
    @staticmethod
    @pytest.mark.parametrize(
        ("plat_list", "statistic", "decimals", "expected"),
        [
            # Mean tests
            ([1, 2, 3, 4, 5], "mean", 1, 3.0),
            ([10, 20, 30], "mean", 0, 20.0),
            # Geometric Mean tests
            ([1, 8], "geometric", 3, 2.828),
            # Median tests
            ([1, 2, 3, 4, 5], "median", 1, 3.0),
            ([1, 2, 3, 4], "median", 1, 2.5),
            ([7, 1, 9, 3, 5], "median", 1, 5.0),
            # Mode tests
            ([1, 2, 2, 3, 4], "mode", 1, 2.0),
            ([5, 4, 6, 8, 9, 1], "mode", 1, 5.0),
        ],
        ids=[
            "mean",
            "mean_no_decimals",
            "geometric",
            "median_odd",
            "median_even",
            "median_unsorted",
            "mode",
            "mode_equal_occurrences",
        ],
    )
    def test_calc_avg_parameterized(
        plat_list: list[int], statistic: AverageKind, decimals: int, expected: float
    ) -> None:
        """Test calc_avg with various inputs."""
        assert average.calc_avg(plat_list, statistic, decimals) == expected

    @staticmethod
    def test_calc_avg_empty_list_raises_error() -> None:
        """Test that NoListingsFoundError is raised for empty list."""
        with pytest.raises(errors.NoListingsFoundError):
            average.calc_avg([], "mean")


class TestInTimeRange:
    TEST_CURRENT_TIME = datetime.datetime(
        2023, 1, 10, 12, 0, 0, tzinfo=datetime.timezone.utc
    )

    @pytest.mark.parametrize(
        ("last_updated", "time_range", "expected_result"),
        [
            # TRUE CASES
            ("2023-01-03T12:00:00+00:00", 7, True),
            ("2023-01-04T12:00:00+00:00", 7, True),
            ("2023-01-10T12:00:00+00:00", 0, True),
            ("2023-01-10T08:00:00+00:00", 0, True),
            ("2023-01-04T12:00:00+00:00", cli_parser.DEFAULT_TIME, True),
            # FALSE CASES
            ("2023-01-02T12:00:00+00:00", 7, False),
            ("2022-12-30T12:00:00+00:00", cli_parser.DEFAULT_TIME, False),
            ("2023-01-11T12:00:00+00:00", 7, False),
        ],
        ids=[
            "last_updated_eq_time-range",
            "last_updated_lt_time-range",
            "last_updated_same_date_and_time",
            "last_updated_earlier_in_day",
            "in_range_w_default_time-range",
            "last_updated_gt_time-range",
            "outside_range_w_default_time-range",
            "time_delta_lt_zero",
        ],
    )
    def test_in_time_range_should_be_bool(
        self,
        last_updated: str,
        time_range: int,
        *,
        expected_result: bool,
    ) -> None:
        """Test cases where the last_updated timestamp is either inside
        or outside the time_range limit."""  # noqa: D205, D209
        assert (
            average.in_time_range(last_updated, self.TEST_CURRENT_TIME, time_range)
            is expected_result
        )

    def test_invalid_isoformat_raises_value_error(self) -> None:
        """Test that ValueError is raised for completely malformed
        ISO-8601 timestamps."""  # noqa: D205, D209
        match_string = "Invalid isoformat string: 'not-a-valid-timestamp'"
        with pytest.raises(ValueError, match=match_string):
            average.in_time_range("not-a-valid-timestamp", self.TEST_CURRENT_TIME)


class TestGetPlatList:
    pass


class TestOutput:
    pass


class TestAverageMain:
    pass
