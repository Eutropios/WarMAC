"""
Logic for http requests, including error checks.

-----------------------------------------------------------------------

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
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import msgspec
import urllib3

from warmac import errors, schema

if TYPE_CHECKING:
    from typing import TypeVar

    ResponseType = TypeVar("ResponseType", schema.OrderResponse, schema.ItemResponse)


HTTP_ERROR_DICT = {
    401: errors.UnauthorizedAccessError,
    403: errors.ForbiddenRequestError,
    404: errors.MalformedURLError,
    405: errors.MethodNotAllowedError,
    429: errors.RateLimitError,
    500: errors.InternalServerError,
}

API_ROOT = "https://api.warframe.market/v2/"

SCHEMA_TO_URL = {
    schema.OrderResponse: "orders/item/",
    schema.ItemResponse: "item/",
}


def item_url(item: str) -> str:
    """
    Replace spaces with underscores and ampersands with "and".

    Args:
        item: String to manipulate.

    Returns:
        Manipulated string.
    """
    return item.strip().lower().replace(" ", "_").replace("&", "and")


def http_code_check(status_code: int) -> None:  # noqa: DOC503
    """
    Check an HTTP status code and raise the appropriate WarMACHTTPError.

    Check if an HTTP status code is 200 and raise the corresponding
    WarMACHTTPError if not.

    Args:
        status_code: HTTP status code to check.

    Raises:
        WarMACHTTPError: Raise an error from HTTP_ERROR_DICT if HTTP
            status code is not 200.
        UnknownError: Raised as fallback if HTTP status code is not in
            HTTP_ERROR_DICT.
    """  # ruff: ignore[docstring-extraneous-exception] # noqa: DOC503
    if status_code == 200:  # ruff: ignore[magic-value-comparison]
        return
    if err := HTTP_ERROR_DICT.get(status_code):
        raise err
    raise errors.UnknownError(status_code)


def get_page(url: str, http_headers: dict[str, str]) -> urllib3.BaseHTTPResponse:
    """
    Make an HTTP request to warframe.market.

    Make an HTTP request to warframe.market using the appropriate
    formatted URL, along with the appropriate http headers. Raise an
    error if the status code is not 200, otherwise, return the requested
    page. This page will need to be decoded into a dictionary.

    Args:
        url: Formatted URL used in the request.
        http_headers: Headers to be used in the HTTP request. Must
            contain at least an "Accept" field.

    Returns:
        Requested JSON.

    Raises:
        WarMACHTTPError: Raise an error from HTTP_ERROR_DICT if HTTP
            status code is not 200.
        UnknownError: Raised as fallback if HTTP status code is not in
            HTTP_ERROR_DICT.
    """  # ruff: ignore[docstring-extraneous-exception] # noqa: DOC502
    page = urllib3.request("GET", url, headers=http_headers, timeout=5)
    http_code_check(page.status)
    return page


def get_data(  # ruff: ignore[non-pep695-generic-function]
    item: str, request_schema: type[ResponseType], http_headers: dict[str, str]
) -> ResponseType:
    """
    Fetch provided item's data from API and decode it using the schema.

    Make a request to the API using the given item. Decode the raw JSON
    response into the WarMAC Struct associated with the provided schema.

    Args:
        item: Item to retrieve.
        request_schema: Schema to use for decoding the API response.
            Determines the expected structure of the returned data.
        http_headers: Headers to be used in the HTTP request.

    Returns:
        WarMAC Struct corresponding to the request_schema.
    """
    url_partial = SCHEMA_TO_URL[request_schema]
    complete_url = f"{API_ROOT}{url_partial}{item_url(item)}"
    raw = get_page(complete_url, http_headers=http_headers).data
    return msgspec.json.decode(raw, type=request_schema)
