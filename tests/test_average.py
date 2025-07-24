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

import argparse
import datetime
from typing import TYPE_CHECKING

# from unittest.mock import MagicMock, Mock
import pytest

from warmac import average, cli_parser, errors, schema

if TYPE_CHECKING:
    from typing import ClassVar, Literal, TypedDict

    from _pytest.mark.structures import ParameterSet

    AverageKind = Literal["geometric", "mean", "median", "mode"]

    class OrderKwargs(TypedDict):
        platinum: int
        type: str
        updated_at: str
        rank: int | None
        subtype: str | None

    class ArgsKwargs(TypedDict):
        use_buyers: str
        maxrank: bool
        radiant: Literal["intact", "radiant"]
        timerange: int

    class ItemKwargs(TypedDict):
        max_rank: int | None


class TestCalcAvg:
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


class TestModArcaneRank:
    @staticmethod
    @pytest.mark.parametrize(
        ("order_rank", "item_max_rank", "use_maxrank", "expected"),
        [
            (None, None, True, True),
            (None, None, False, True),
            (None, 5, True, True),
            (None, 10, False, True),
            (0, None, True, True),
            (5, None, False, True),
        ],
        ids=[
            "both_none_maxrank",
            "both_none_unranked",
            "order_rank_none_maxrank",
            "order_rank_none_unranked",
            "item_max_rank_none_maxrank",
            "item_max_rank_none_unranked",
        ],
    )
    def test_both_none(
        order_rank: int | None,
        item_max_rank: int | None,
        *,
        use_maxrank: bool,
        expected: bool,
    ) -> None:
        """Test that True is always returned if at least one of
        order_rank and item_max_rank is None, regardless of the argument
        passed for use_maxrank."""  # noqa: D205, D209
        assert (
            average.check_mod_arcane_rank(
                order_rank, item_max_rank, use_maxrank=use_maxrank
            )
            == expected
        )

    @staticmethod
    @pytest.mark.parametrize(
        ("order_rank", "item_max_rank", "use_maxrank", "expected"),
        [
            (5, 5, True, True),
            (4, 5, True, False),
            (0, 5, True, False),
            (0, 0, True, True),
            # -- use_maxrank is False --
            (5, 5, False, False),
            (4, 5, False, False),
            (0, 1, False, True),
            (0, 0, False, True),
        ],
        ids=[
            "order_eq_item_max_w_maxrank",
            "order_lt_item_max_w_maxrank",
            "order_0_w_maxrank",
            "both_0_w_maxrank",
            "order_eq_item_max_unranked",
            "order_non-zero_unranked",
            "order_0_w_unranked",
            "both_0_w_unranked",
        ],
    )
    def test_non_none_params_use_maxrank(
        order_rank: int, item_max_rank: int, *, use_maxrank: bool, expected: bool
    ) -> None:
        """Test various cases of order_rank against item_max_rank
        depending on use_maxrank."""  # noqa: D205, D209
        assert (
            average.check_mod_arcane_rank(
                order_rank, item_max_rank, use_maxrank=use_maxrank
            )
            == expected
        )


class TestRelicSubtype:
    @staticmethod
    @pytest.mark.parametrize(
        ("subtype", "use_radiant", "expected"),
        [
            (None, "intact", True),
            (None, "radiant", True),
            ("intact", "intact", True),
            ("radiant", "intact", False),
            ("some_other_string", "intact", False),
        ],
        ids=[
            "none_subtype_w_intact",
            "none_subtype_w_radiant",
            "subtypes_match",
            "subtypes_dont_match",
            "invalid_subtype",
        ],
    )
    def test_check_relic_subtype(
        subtype: str | None,
        use_radiant: Literal["intact", "radiant"],
        *,
        expected: bool,
    ) -> None:
        """Test various combinations of subtype and use_radiant."""
        result = average.check_relic_subtype(subtype, use_radiant)
        assert result == expected


def order_kwargs(
    platinum: int = 100,
    order_type: str = "sell",
    updated_at: str = "2025-07-23T09:00:00Z",
    rank: int | None = None,
    subtype: str | None = "intact",
) -> OrderKwargs:
    """Construct a dictionary to be used in creating a
    schema.OrderWithUser object."""  # noqa: D205, D209
    return {
        "platinum": platinum,
        "type": order_type,
        "updated_at": updated_at,
        "rank": rank,
        "subtype": subtype,
    }


def item_info_kwargs(max_rank: int | None = None) -> ItemKwargs:
    """Construct a dictionary to be used in creating a schema.Item
    object."""  # noqa: D205, D209
    return {"max_rank": max_rank}


def args_kwargs(
    use_buyers: str = "sell",
    radiant: Literal["intact", "radiant"] = "intact",
    timerange: int = cli_parser.DEFAULT_TIME,
    *,
    maxrank: bool = False,
) -> ArgsKwargs:
    """Construct a dictionary to be used in-place of CLI arguments."""
    return {
        "use_buyers": use_buyers,
        "maxrank": maxrank,
        "radiant": radiant,
        "timerange": timerange,
    }


@pytest.fixture
def fixed_current_time() -> datetime.datetime:
    """Fixture that returns a set datetime object."""
    return datetime.datetime(2025, 7, 23, 10, 0, 0, 0, datetime.timezone.utc)


user = schema.UserShort(
    id="martin",
    ingame_name="martin123",
    reputation=1,
    platform="ps4",
    crossplay=True,
)


class TestFilterOrderProgrammatic:
    test_cases: ClassVar[list[ParameterSet]] = [
        pytest.param(
            order_kwargs(),  # 100, sell, time, None (rank), None (subtype)
            item_info_kwargs(),  # None (maxrank)
            args_kwargs(),  # sell, intact, default_time, False (maxrank)
            True,
            # same order type, in timerange, no relic filter,
            # not mod or arcane
            id="all_passing_conditions",
        ),
        pytest.param(
            order_kwargs(order_type="buy"),  # 100, buy, time, None(rank), None(subtype)
            item_info_kwargs(),  # None (maxrank)
            args_kwargs(),  # sell, intact, default_time, False (maxrank)
            False,
            # different order type. Should fail at that step in func
            id="fail_different_order_type",
        ),
        pytest.param(
            order_kwargs(rank=1),  # 100, buy, time, rank=1, None(subtype)
            item_info_kwargs(max_rank=5),  # max_rank is 5
            args_kwargs(maxrank=False),  # unranked
            False,
            id="fail_rank_mismatch_expected_unranked",
        ),
        pytest.param(
            order_kwargs(rank=1),  # 100, buy, time, rank=1, None(subtype)
            item_info_kwargs(max_rank=5),  # max_rank is 5
            args_kwargs(maxrank=True),  # maxrank
            False,
            id="fail_rank_mismatch_expected_maxrank",
        ),
        pytest.param(
            order_kwargs(updated_at="2025-07-08T09:00:00Z"),
            item_info_kwargs(),
            args_kwargs(timerange=10),
            False,
            id="fail_order_outside_timerange",
        ),
        pytest.param(
            order_kwargs(updated_at="2025-07-13T09:00:00Z"),  # same as current_time
            item_info_kwargs(),
            args_kwargs(timerange=10),
            True,
            id="pass_order_time_eq_timerange",
        ),
        pytest.param(
            order_kwargs(subtype="radiant"),  # radiant subtype
            item_info_kwargs(),
            args_kwargs(timerange=10),  # intact
            False,
            id="fail_relic_subtype_mismatch",
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize(
        (
            "order_kwargs",
            "item_info_kwargs",
            "args_kwargs",
            "expected_result",
        ),
        test_cases,
    )
    def test_filter_order(
        order_kwargs: OrderKwargs,
        item_info_kwargs: ItemKwargs,
        args_kwargs: ArgsKwargs,
        fixed_current_time: datetime.datetime,
        *,
        expected_result: bool,
    ) -> None:
        """Test various objects in filter to see if they hold up."""
        order = schema.OrderWithUser(
            id="bob",
            quantity=1,
            created_at="2025-06-13T09:00:00Z",
            item_id="joe",
            user=user,
            **order_kwargs,
        )
        item_info = schema.Item(id="gary", slug="foo", tags=[], **item_info_kwargs)
        args = argparse.Namespace(**args_kwargs)

        result = average.filter_order(order, item_info, fixed_current_time, args)
        assert result == expected_result


class TestFilterOrder:
    pass


class TestGetPlatList:
    pass


class TestOutput:
    pass


class TestAverageMain:
    pass
