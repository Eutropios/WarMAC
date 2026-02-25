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

import pytest

from warmac import average, config, errors, schema

if TYPE_CHECKING:
    from typing import ClassVar, Literal, TypedDict
    from unittest.mock import Mock

    from _pytest.mark.structures import ParameterSet

    from warmac.config import AverageType

    class OrderKwargs(TypedDict):
        platinum: int
        order_type: str
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
        "order_type": order_type,
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
    timerange: int = config.DEFAULT_TIME,
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


user = schema.UserShort(
    id="martin",
    ingame_name="martin123",
    reputation=1,
    platform="ps4",
    crossplay=True,
)


class TestCalcAvg:
    @staticmethod
    @pytest.mark.parametrize(
        ("plat_list", "statistic", "decimals", "expected"),
        [
            # Mean tests
            ([5, 3, 1, 2, 4], "mean", 1, 3.0),
            ([10, 20, 30], "mean", 0, 20.0),
            # Geometric Mean tests
            ([1, 8], "geometric", 3, 2.828),
            # Median tests
            ([5, 3, 1, 2, 4], "median", 1, 3.0),
            ([1, 2, 3, 4], "median", 1, 2.5),
            # Mode tests
            ([1, 2, 2, 3, 4], "mode", 1, 2.0),
            ([5, 4, 6, 8, 9, 1], "mode", 1, 5.0),
        ],
        ids=[
            "mean_unsorted",
            "mean_no_decimals",
            "geometric",
            "median_unsorted",
            "median_even",
            "mode_no_dupes",
            "mode_equal_occurrences",
        ],
    )
    def test_calculate_average_parameterized(
        plat_list: list[int], statistic: AverageType, decimals: int, expected: float
    ) -> None:
        """Test calculate_average with various inputs."""
        assert average.calculate_average(plat_list, statistic, decimals) == expected

    @staticmethod
    def test_calculate_average_empty_list_raises_error() -> None:
        """Test that NoListingsFoundError is raised for empty list."""
        with pytest.raises(errors.NoListingsFoundError):
            average.calculate_average([], "mean")


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
            ("2023-01-04T12:00:00+00:00", 10, True),
            # FALSE CASES
            ("2023-01-02T12:00:00+00:00", 7, False),
            ("2023-01-11T12:00:00+00:00", 7, False),
        ],
        ids=[
            "last_updated_eq_time-range",
            "last_updated_lt_time-range",
            "last_updated_same_date_and_time",
            "last_updated_earlier_in_day",
            "in_range_w_default_time-range",
            "last_updated_gt_time-range",
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
        match_string = (
            r"Invalid isoformat string: 'not-a-valid-timestamp'|Unknown string format:"
            r" not-a-valid-timestamp"
        )
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
            # use_maxrank is True
            (5, 5, True, True),
            (4, 5, True, False),
            (0, 5, True, False),
            (0, 0, True, True),
            # use_maxrank is False
            (5, 5, False, False),
            (4, 5, False, False),
            (0, 1, False, True),
            (0, 0, False, True),
        ],
        ids=[
            "both_none_maxrank",
            "both_none_unranked",
            "order_rank_none_maxrank",
            "order_rank_none_unranked",
            "item_max_rank_none_maxrank",
            "item_max_rank_none_unranked",
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
    def test_various_combinations(
        order_rank: int | None,
        item_max_rank: int | None,
        *,
        use_maxrank: bool,
        expected: bool,
    ) -> None:
        """Test that various inputs."""
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


class TestGetPlatList:
    @staticmethod
    @pytest.mark.parametrize(
        (
            "order_data_params",
            "item_info_params",
            "args_params",
            "expected_plat_list",
        ),
        [
            pytest.param(
                [
                    order_kwargs(platinum=100, order_type="sell"),
                    order_kwargs(platinum=50, order_type="buy"),
                ],
                item_info_kwargs(),
                args_kwargs(use_buyers="sell"),
                [100],
                id="order_types_match",
            ),
            pytest.param(
                [
                    order_kwargs(platinum=100, subtype="intact"),
                    order_kwargs(platinum=200, subtype="radiant"),
                ],
                item_info_kwargs(),
                args_kwargs(radiant="intact"),
                [100],
                id="intact_subtype_matches",
            ),
            pytest.param(
                [
                    order_kwargs(platinum=100, subtype="intact"),
                    order_kwargs(platinum=200, subtype="radiant"),
                ],
                item_info_kwargs(),
                args_kwargs(radiant="radiant"),
                [200],
                id="radiant_subtype_matches",
            ),
            pytest.param(
                [
                    order_kwargs(platinum=100, updated_at="2025-07-22T09:00:00Z"),
                    order_kwargs(platinum=50, updated_at="2025-07-01T09:00:00Z"),
                ],
                item_info_kwargs(),
                args_kwargs(timerange=7),
                [100],
                id="order_in_time_range",
            ),
            pytest.param(
                [order_kwargs(platinum=100, rank=5), order_kwargs(platinum=50, rank=0)],
                item_info_kwargs(max_rank=5),
                args_kwargs(maxrank=True),
                [100],
                id="order_is_maxrank",
            ),
            pytest.param(
                [order_kwargs(platinum=100, rank=5), order_kwargs(platinum=50, rank=0)],
                item_info_kwargs(max_rank=5),
                args_kwargs(maxrank=False),
                [50],
                id="order_is_unranked",
            ),
            pytest.param(
                [],
                item_info_kwargs(),
                args_kwargs(),
                [],
                id="empty_order_data_does_nothing",
            ),
            pytest.param(
                [
                    order_kwargs(platinum=10),
                    order_kwargs(platinum=20),
                    order_kwargs(platinum=30),
                ],
                item_info_kwargs(),
                args_kwargs(),
                [10, 20, 30],
                id="all_orders_pass",
            ),
            pytest.param(
                [
                    order_kwargs(platinum=10, order_type="buy"),
                    order_kwargs(platinum=20, updated_at="2024-01-01T00:00:00Z"),
                ],
                item_info_kwargs(),
                args_kwargs(use_buyers="sell", timerange=1),
                [],
                id="no_orders_pass",
            ),
        ],
    )
    def test_filtered_plat_list(
        order_data_params: list[OrderKwargs],
        item_info_params: ItemKwargs,
        args_params: ArgsKwargs,
        fixed_current_time: datetime.datetime,
        expected_plat_list: list[int],
    ) -> None:
        """Test filtered_plat_list with various filtering scenarios."""
        orders = [
            schema.OrderWithUser(
                id="some_id",
                quantity=1,
                created_at="2025-06-13T09:00:00Z",
                item_id="some_item_id",
                user=user,
                **kw,
            )
            for kw in order_data_params
        ]

        item_info = schema.Item(
            id="item_id", slug="item_slug", tags=[], **item_info_params
        )
        args = argparse.Namespace(**args_params)
        result = average.filtered_plat_list(orders, item_info, fixed_current_time, args)
        assert result == expected_plat_list


class TestFormatOutput:
    @staticmethod
    @pytest.mark.parametrize(
        ("statistic", "item_name", "stat_value", "plat_list", "porcelain", "expected"),
        [
            (
                "mode",
                "Gara Prime Blueprint",
                75.0,
                [70, 75, 75, 80],
                False,
                "Mode Price:            75.0 platinum",
            ),
            (
                "mean",
                "Andromeda And Andromeda",
                12.3,
                [10, 15],
                False,
                "Item:                  Andromeda & Andromeda",
            ),
            (
                "mean",
                "Precision Test",
                123.45678,
                [120, 126],
                False,
                "Mean Price:            123.45678 platinum",
            ),
            (
                "median",
                "Atlas Prime Set",
                100.0,
                [90, 95, 100, 105, 110],
                True,
                "Atlas Prime Set:5:100.0:90:110:5",
            ),
            ("median", "Solo Item", 70.0, [70], True, "Solo Item:5:70.0:70:70:1"),
            (
                "mean",
                "Some Item",
                987.654321,
                [900, 1000],
                True,
                "Some Item:5:987.654321:900:1000:2",
            ),
        ],
        ids=[
            # Detailed
            "normal_detailed",
            "and_replacement_detailed",
            "precision_gt_two_detailed",
            # Porcelain
            "normal_porcelain",
            "single-item_porcelain",
            "precision_gt_two_porcelain",
        ],
    )
    def test_detailed_output(  # noqa: PLR0913, PLR0917
        statistic: AverageType,
        item_name: str,
        stat_value: float,
        plat_list: list[int],
        expected: str,
        mock_args: argparse.Namespace,
        *,
        porcelain: bool,
    ) -> None:
        """Test detailed output against various statistics and item."""
        mock_args.detailed_report = True
        mock_args.statistic = statistic
        mock_args.item = item_name
        mock_args.timerange = 5
        mock_args.porcelain = porcelain
        actual_output = average.format_output(stat_value, plat_list, mock_args)
        if porcelain:
            assert actual_output == expected
        else:
            fixed_item_name = (
                item_name.title().replace("_", " ").replace(" And ", " & ")
            )
            max_price = max(plat_list)
            min_price = min(plat_list)
            num_orders = len(plat_list)

            assert f"Item:                  {fixed_item_name}" in actual_output
            assert expected in actual_output
            assert f"Max Price:             {max_price:.0f} platinum" in actual_output
            assert f"Min Price:             {min_price:.0f} platinum" in actual_output
            assert f"Number of Orders:      {num_orders}" in actual_output

    @staticmethod
    def test_empty_plat_list_raises_error(mock_args: argparse.Namespace) -> None:
        """
        Test that error is raised if format_output is given empty list.

        It should be noted that format_output should not be called with
        an empty plat_list, as calculate_average would raise an error
        and cause the program to exit.
        """
        stat = 0.0
        plat_list: list[int] = []
        mock_args.item = "Nonexistent Item"
        mock_args.detailed_report = True

        with pytest.raises(
            ValueError,
            match=(
                r"(max\(\) iterable argument is empty)|(max\(\) arg is an empty "
                r"sequence)"
            ),
        ):
            average.format_output(stat, plat_list, mock_args)

    @staticmethod
    def test_format_non_detailed_report(mock_args: argparse.Namespace) -> None:
        """Test that format_output only returns the calculated statistic
        if args.detailed_report is False."""  # noqa: D205, D209
        mock_args.detailed_report = False
        statistic_value = 20
        plat_list = [10, 20, 30]
        actual_output = average.format_output(statistic_value, plat_list, mock_args)
        expected_output = "20"
        assert actual_output == expected_output


class TestGetRequiredData:
    @staticmethod
    def test_get_required_data_success(
        mocker: Mock,
        mock_item_response: schema.ItemResponse,
        mock_order_response: schema.OrderResponse,
        mock_http_headers: dict[str, str],
    ) -> None:
        """Test that get_required_data successfully calls fetch_data
        twice and returns the expected tuple of data."""  # noqa: D205, D209
        mock_get_data = mocker.patch("warmac.fetch_data.get_data")
        mock_get_data.side_effect = [mock_item_response, mock_order_response]
        item_name = "mock_item"
        item_data, order_data = average.get_required_data(item_name, mock_http_headers)
        assert mock_get_data.call_count == 2  # noqa: PLR2004
        mock_get_data.assert_has_calls([
            mocker.call(item_name, schema.ItemResponse, mock_http_headers),
            mocker.call(item_name, schema.OrderResponse, mock_http_headers),
        ])
        assert item_data == mock_item_response
        assert order_data == mock_order_response


class TestProcessData:
    @staticmethod
    def test_process_data_success(  # noqa: PLR0913, PLR0917
        mocker: Mock,
        mock_args: argparse.Namespace,
        mock_http_headers: dict[str, str],
        fixed_current_time: datetime.datetime,
        mock_item_response: schema.ItemResponse,
        mock_order_response: schema.OrderResponse,
    ) -> None:
        """Test that process_data correctly calculates and formats the
        output with valid data."""  # noqa: D205, D209
        mocker.patch(
            "warmac.average.get_required_data",
            return_value=(mock_item_response, mock_order_response),
        )
        result = average.process_data(mock_args, mock_http_headers, fixed_current_time)
        assert result == "110.0"

    @staticmethod
    def test_process_data_no_listings_found(  # noqa: PLR0913, PLR0917
        mocker: Mock,
        mock_args: argparse.Namespace,
        mock_http_headers: dict[str, str],
        fixed_current_time: datetime.datetime,
        mock_item_response: schema.ItemResponse,
        mock_order_response: schema.OrderResponse,
    ) -> None:
        """Test that process_data raises NoListingsFoundError when
        filtered platinum list is empty."""  # noqa: D205, D209
        mocker.patch(
            "warmac.average.get_required_data",
            return_value=(mock_item_response, mock_order_response),
        )
        mocker.patch("warmac.average.filtered_plat_list", return_value=[])

        with pytest.raises(errors.NoListingsFoundError):
            average.process_data(mock_args, mock_http_headers, fixed_current_time)
