"""
tests.conftest
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

Fixture file
"""  # noqa: D205, D400

from __future__ import annotations

import argparse
import datetime
from typing import TYPE_CHECKING

import pytest

from warmac import schema

if TYPE_CHECKING:
    from unittest.mock import MagicMock

user = schema.UserShort(
    id="martin",
    ingame_name="martin123",
    reputation=1,
    platform="ps4",
    crossplay=True,
)


@pytest.fixture
def mock_get_page(mocker: MagicMock) -> object:
    """Fixture that patches fetch_data.get_page, preventing real HTTP
    requests during tests."""  # noqa: D205, D209
    return mocker.patch("warmac.fetch_data.get_page")


@pytest.fixture
def fixed_current_time() -> datetime.datetime:
    """Fixture that returns a set datetime object."""
    return datetime.datetime(2025, 7, 23, 10, 0, 0, 0, datetime.timezone.utc)


@pytest.fixture
def mock_args() -> argparse.Namespace:
    """Fixture to create a mock argparse.Namespace object."""
    return argparse.Namespace(
        statistic="mean",
        item="mock_item",
        porcelain=False,
        radiant=None,
        use_buyers="buy",
        maxrank=False,
        timerange=30,
        ndigits=2,
        detailed_report=False,
    )


@pytest.fixture
def mock_item_response() -> schema.ItemResponse:
    """Fixture for a mock ItemResponse object."""
    return schema.ItemResponse(
        api_version="1",
        data=schema.Item(
            id="mock_id",
            max_rank=5,
            tags=["foo"],
            slug="431",
        ),
    )


@pytest.fixture
def mock_order_response() -> schema.OrderResponse:
    """Fixture for a mock OrderResponse object."""
    return schema.OrderResponse(
        api_version="",
        data=[
            schema.OrderWithUser(
                id="order1",
                item_id="1234",
                type="buy",
                created_at="2025-07-09T12:00:00Z",
                updated_at="2025-07-09T12:00:00Z",
                platinum=100,
                quantity=1,
                rank=0,
                user=user,
                subtype=None,
            ),
            schema.OrderWithUser(
                id="order2",
                type="sell",
                created_at="2025-07-29T12:00:00Z",
                updated_at="2025-07-29T12:00:00Z",
                platinum=150,
                quantity=1,
                rank=0,
                user=user,
                subtype=None,
                item_id="431",
            ),
            schema.OrderWithUser(
                id="order3",
                type="buy",
                created_at="2025-07-15T12:00:00Z",
                updated_at="2025-07-15T12:00:00Z",
                platinum=120,
                quantity=1,
                rank=0,
                user=user,
                subtype=None,
                item_id="849",
            ),
        ],
    )


@pytest.fixture
def mock_http_headers() -> dict[str, str]:
    """Fixture that provides a basic set of HTTP headers."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    }
