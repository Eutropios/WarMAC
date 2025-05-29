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

import pytest
import urllib3

from warmac import errors, fetch_data

if TYPE_CHECKING:
    from unittest.mock import MagicMock

headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Language": "en",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Platform": "ps4",
}

# get_page:
#  url is not correctly formatted throws error. Test each case
#  test headers are accepted by wfm
# figure out how to induce http codes
# correct


class TestGetData:
    @staticmethod
    def test_param_and_return_type_match() -> None:
        pass


# test if the param type matches return type
# test if schema_to_url correctly throws error
# test if schema_to_url throws no error on valid type
# test if get_data returns a decoded struct on valid req
class TestGetPage:
    @staticmethod
    def test_get_page_returns_response_on_200(mocker: MagicMock) -> None:
        mock_response = mocker.MagicMock(spec=urllib3.BaseHTTPResponse)
        mock_response.status = 200
        mock_response.data = b"{'message': 'success'}"  # Example data

        mock_urllib_request = mocker.patch(
            "urllib3.request", return_value=mock_response
        )
        result = fetch_data.get_page("http://example.com/test", headers=headers)
        mock_urllib_request.assert_called_once_with(
            "GET", "http://example.com/test", headers=headers, timeout=5
        )
        assert result is mock_response
        assert result.data == b"{'message': 'success'}"

    @staticmethod
    def test_get_page_raises_forbidden_error_on_403_status(mocker: MagicMock) -> None:
        """Test that get_page correctly propagates a
        ForbiddenRequestError when urllib3.request returns a 403
        status."""  # noqa: D205, D209
        mock_response = mocker.MagicMock(spec=urllib3.BaseHTTPResponse)
        mock_response.status = 403
        mocker.patch("urllib3.request", return_value=mock_response)
        with pytest.raises(errors.ForbiddenRequestError):
            fetch_data.get_page("http://example.com/forbidden", headers=headers)

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
    def test_get_page_raises_correct_error_for_status(
        mocker: MagicMock,
        status_code: int,
        expected_error_type: type[errors.WarMACHTTPError],
    ) -> None:
        """Test that get_page correctly propagates various HTTP errors
        based on the status code returned by urllib3.request."""  # noqa: D205, D209
        mock_response = mocker.MagicMock(spec=urllib3.BaseHTTPResponse)
        mock_response.status = status_code

        mocker.patch("urllib3.request", return_value=mock_response)

        with pytest.raises(expected_error_type) as excinfo:
            fetch_data.get_page("http://example.com/error_test", headers=headers)

        if expected_error_type is errors.UnknownError:
            expected_message = (
                f"Unknown Error; HTTP Code {status_code}. Please open a "
                "new issue on the Github page (link in README.md file)."
            )
            assert str(excinfo.value) == expected_message

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
        """Verify http_code_check raises the correct specific error."""
        with pytest.raises(expected_error):
            fetch_data.http_code_check(status_code)

    @staticmethod
    def test_http_code_check_raises_unknown_error_for_unmapped_code() -> None:
        """Verify http_code_check raises UnknownError for unmapped
        codes."""  # noqa: D205, D209
        with pytest.raises(errors.UnknownError) as excinfo:
            fetch_data.http_code_check(499)
        assert str(excinfo.value) == (
            "Unknown Error; HTTP Code 499. "
            "Please open a new issue on the Github page (link in README.md file)."
        )
