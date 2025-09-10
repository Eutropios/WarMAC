"""
tests.test_cli_parser
~~~~~~~~~~~~~~~~~~~~~

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

Test file for cli_parser.py
"""  # noqa: D205, D400

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, Mock

import msgspec
import pytest
import urllib3

from warmac import errors, fetch_data, schema

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from warmac.fetch_data import ResponseKind


http_headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Language": "en",
    "Platform": "ps4",
}


class TestItemUrl:
    @staticmethod
    @pytest.mark.parametrize(
        ("input_item", "expected_output"),
        [
            ("Gauss Prime Set", "gauss_prime_set"),
            ("Silva & aegis", "silva_and_aegis"),
            ("  ack & BRUNT ", "ack_and_brunt"),
            ("", ""),
            ("   ", ""),
            ("&&&", "andandand"),  # cspell:disable-line
            ("B1g (#_|NGv$ ", "b1g_(#_|ngv$"),
        ],
        ids=[
            "space_to_underscore",
            "ampersand_to_and",
            "strip_leading_spaces",
            "empty_str",
            "sstrip_before_space_replace",  # cspell:disable-line
            "all_ampersand_to_and",
            "random_symbols",
        ],
    )
    def test_item_url_transformations(input_item: str, expected_output: str) -> None:
        """Test that function strips preceding and succeeding
        whitespace, makes characters lowercase, replaces spaces with
        underscores, and replaces ampersands with "and"."""  # noqa: D205, D209
        assert fetch_data.item_url(input_item) == expected_output


class TestGetData:
    @staticmethod
    def _get_expected_url(item_name: str, schema_type: ResponseKind) -> str:
        return (
            f"{fetch_data.API_ROOT}{fetch_data.SCHEMA_TO_URL[schema_type]}{item_name}"
        )

    @staticmethod
    @pytest.mark.parametrize(
        ("schema_type", "expected_url_fragment"),
        [
            (schema.OrderResponse, "orders/item/"),
            (schema.ItemResponse, "item/"),
        ],
    )
    def test_schema_in_dict_gives_correct_url_fragment(
        schema_type: ResponseKind, expected_url_fragment: str
    ) -> None:
        """Test that strings in the SCHEMA_TO_URL dict are correct."""
        assert fetch_data.SCHEMA_TO_URL[schema_type] == expected_url_fragment

    def test_get_data_success_item_response(self, mock_get_page: MagicMock) -> None:
        """Verify get_data successfully fetches and decodes requested
        data for an ItemResponse."""  # noqa: D205, D209
        test_item_name = "rhino_prime_set"
        mock_raw_data = b"""
            {
                "apiVersion": "2.1.0",
                "error": null,
                "data": {
                    "id": "123",
                    "slug": "rhino_prime_set",
                    "ducats": 100,
                    "tags": [
                        "prime"
                    ]
                }
            }
        """
        mock_http_response = Mock()
        mock_http_response.data = mock_raw_data
        mock_get_page.return_value = mock_http_response

        expected_url = self._get_expected_url(test_item_name, schema.ItemResponse)
        result = fetch_data.get_data(test_item_name, schema.ItemResponse, http_headers)

        mock_get_page.assert_called_once_with(expected_url, http_headers=http_headers)
        assert isinstance(result, schema.ItemResponse)
        assert result.api_version == "2.1.0"
        assert isinstance(result.data, schema.Item)
        assert result.data.id == "123"
        assert result.data.slug == "rhino_prime_set"
        assert result.error is None

    def test_get_data_success_order_response(self, mock_get_page: MagicMock) -> None:
        """Verify get_data successfully fetches and decodes requested
        data for an OrderResponse."""  # noqa: D205, D209
        test_item_name = "prime_fissure_orders"
        mock_raw_data = b"""
            {
                "apiVersion": "2.1.0",
                "data": [
                    {
                        "id": "a",
                        "type": "buy",
                        "platinum": 10,
                        "quantity": 1,
                        "perTrade": 1,
                        "createdAt": "2024-06-16T10:00:00.000Z",
                        "cyanStars": null,
                        "rank": 0,
                        "updatedAt": "2024-06-16T10:05:00.000Z",
                        "vosfor": 20,
                        "subtype": "relic",
                        "itemId": "5a4dd0561502476579f18a5e",
                        "charges": null,
                        "amberStars": null,
                        "user": {
                            "id": "user1",
                            "ingameName": "joe",
                            "reputation": 10,
                            "platform": "ps4",
                            "crossplay": true
                        }
                    },
                    {
                        "id": "b",
                        "type": "sell",
                        "platinum": 20,
                        "quantity": 5,
                        "perTrade": 5,
                        "createdAt": "2024-06-15T12:00:00.000Z",
                        "cyanStars": 3,
                        "vosfor": null,
                        "updatedAt": "2024-06-15T12:10:00.000Z",
                        "rank": 3,
                        "subtype": null,
                        "itemId": "5e1f0e42f61e88002a2432d5",
                        "charges": 3,
                        "amberStars": 2,
                        "user": {
                            "id": "user2",
                            "ingameName": "JaneDoe",
                            "reputation": 50,
                            "platform": "pc",
                            "crossplay": false
                        }
                    }
                ]
            }
        """

        mock_http_response = Mock()
        mock_http_response.data = mock_raw_data
        mock_get_page.return_value = mock_http_response

        expected_url = self._get_expected_url(test_item_name, schema.OrderResponse)

        result = fetch_data.get_data(test_item_name, schema.OrderResponse, http_headers)

        mock_get_page.assert_called_once_with(expected_url, http_headers=http_headers)
        assert isinstance(result, schema.OrderResponse)

        assert result.api_version == "2.1.0"
        assert result.error is None

        assert isinstance(result.data[0], schema.OrderWithUser)
        assert result.data[0].id == "a"
        assert result.data[0].platinum == 10  # noqa: PLR2004
        assert result.data[0].type == "buy"

    def test_get_data_http_error_from_get_page(self, mock_get_page: MagicMock) -> None:
        """Test that get_data correctly propagates a MalformedURLError
        raised by get_page."""  # noqa: D205, D209
        test_item_name = "non_existent_item"
        mock_get_page.side_effect = errors.MalformedURLError
        with pytest.raises(errors.MalformedURLError):
            fetch_data.get_data(test_item_name, schema.ItemResponse, http_headers)
        expected_url = self._get_expected_url(test_item_name, schema.ItemResponse)
        mock_get_page.assert_called_once_with(expected_url, http_headers=http_headers)

    def test_get_data_malformed_data_error(self, mock_get_page: MagicMock) -> None:
        """Test that get_data raises a msgspec.ValidationError if raw
        response data is a valid JSON, but does not conform to the
        expected schema."""  # noqa: D205, D209
        test_item_name = "missing_api_version_item"
        # missing api_version field to induce error
        mock_raw_data = b"""
            {
                "data": {
                    "id": "123",
                    "slug": "test_item",
                    "tags": [
                    "prime"
                    ]
                },
                "error": null
            }
        """

        mock_http_response = Mock()
        mock_http_response.data = mock_raw_data
        mock_get_page.return_value = mock_http_response

        with pytest.raises(msgspec.ValidationError) as exc_info:
            fetch_data.get_data(test_item_name, schema.ItemResponse, http_headers)

        assert "Object missing required field `apiVersion`" in str(exc_info.value)

        expected_url = self._get_expected_url(test_item_name, schema.ItemResponse)
        mock_get_page.assert_called_once_with(expected_url, http_headers=http_headers)


class TestGetPage:
    @staticmethod
    def test_get_page_returns_response_on_200(mocker: MagicMock) -> None:
        """Verify that a response is returned when HTTP code is 200."""
        mock_response = mocker.MagicMock(spec=urllib3.BaseHTTPResponse)
        mock_response.status = 200
        mock_response.data = b"{'message': 'success'}"

        mock_urllib_request = mocker.patch(
            "urllib3.request", return_value=mock_response
        )
        result = fetch_data.get_page(
            "https://httpstat.us/200", http_headers=http_headers
        )
        mock_urllib_request.assert_called_once_with(
            "GET", "https://httpstat.us/200", headers=http_headers, timeout=5
        )
        assert result is mock_response
        assert result.data == b"{'message': 'success'}"

    @staticmethod
    @pytest.mark.parametrize(
        ("status_code", "expected_error_type"),
        [
            (401, errors.UnauthorizedAccessError),
            (403, errors.ForbiddenRequestError),
            (404, errors.MalformedURLError),
            (405, errors.MethodNotAllowedError),
            (500, errors.InternalServerError),
            (418, errors.UnknownError),  # random unmapped code
        ],
    )
    def test_get_page_correctly_propagates_errors(
        mocker: MagicMock,
        status_code: int,
        expected_error_type: type[errors.WarMACHTTPError],
    ) -> None:
        """Test that get_page correctly propagates various HTTP errors
        based on the status code returned by urllib3.request."""  # noqa: D205, D209
        mock_response = mocker.MagicMock(spec=urllib3.BaseHTTPResponse)
        mock_response.status = status_code
        mocker.patch("urllib3.request", return_value=mock_response)
        with pytest.raises(expected_error_type) as exc_info:
            fetch_data.get_page(
                f"https://httpstat.us/{status_code}", http_headers=http_headers
            )

        if expected_error_type is errors.UnknownError:
            expected_message = (
                f"Unknown Error - HTTP Code {status_code}: Please open a new issue on "
                "the GitHub page (link in README.md file)."
            )
            assert str(exc_info.value) == expected_message


class TestHTTPCodeCheck:
    @staticmethod
    @pytest.mark.parametrize(
        ("status_code", "expected_error"),
        [
            (401, errors.UnauthorizedAccessError),
            (403, errors.ForbiddenRequestError),
            (404, errors.MalformedURLError),
            (405, errors.MethodNotAllowedError),
            (500, errors.InternalServerError),
        ],
    )
    def test_http_code_check_raises_mapped_errors(
        status_code: int, expected_error: type[errors.WarMACHTTPError]
    ) -> None:
        """Verify http_code_check raises the correct error."""
        with pytest.raises(expected_error):
            fetch_data.http_code_check(status_code)

    @staticmethod
    def test_http_code_check_raises_unknown_error_for_unmapped_code() -> None:
        """Verify http_code_check raises UnknownError for unmapped
        codes."""  # noqa: D205, D209
        with pytest.raises(errors.UnknownError) as exc_info:
            fetch_data.http_code_check(499)
        assert str(exc_info.value) == (
            "Unknown Error - HTTP Code 499: Please open a new issue on the GitHub page "
            "(link in README.md file)."
        )
