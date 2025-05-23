"""
warmac.fetch_data
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

Logic for http requests, including error checks.
"""  # noqa: D205, D400

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import msgspec
import urllib3

from warmac import errors, schema

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Final, TypeVar

    T = TypeVar("T", bound=schema.Base)


HTTP_ERROR_DICT: Final[Mapping[int, type[errors.WarMACHTTPError]]] = {
    401: errors.UnauthorizedAccessError,
    403: errors.ForbiddenRequestError,
    404: errors.MalformedURLError,
    405: errors.MethodNotAllowedError,
    500: errors.InternalServerError,
}

headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Language": "en",
    "Content-Type": "application/json",
    "Host": "api.warframe.market",
    "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/116.0",
    "Platform": "ps4",
}

API_ROOT = "https://api.warframe.market/v2/"

SCHEMA_TO_URL: dict[type[schema.Base], str] = {
    schema.OrderResponse: "orders/item/",
    schema.ItemResponse: "item/",
}


def get_page(url: str, headers: dict[str, str]) -> urllib3.BaseHTTPResponse:
    """
    Make an HTTP request to warframe.market.

    Make an HTTP request to warframe.market using the appropriate
    formatted URL, along with the appropriate headers. Raise an error if
    the status code is not 200, otherwise, return the requested page.
    This page will need to be decoded into a dictionary.

    :param url: The formatted URL used in the request.
    :param headers: The headers to be used in the HTTP request.
    :raises HTTP_ERROR_DICT: Raise an error from HTTP_ERROR_DICT given
        the HTTP response code.
    :raises errors.UnknownError: Fallback raised if the error code is
        not present in HTTP_ERROR_DICT.
    :return: The requested JSON.
    """
    page = urllib3.request("GET", url, headers=headers, timeout=5)
    status = page.status
    if status == 200:  # noqa: PLR2004
        return page
    with contextlib.suppress(KeyError):
        raise HTTP_ERROR_DICT[status]
    raise errors.UnknownError(status)


def get_data(item: str, request_schema: type[T]) -> T:
    """
    Fetch provided item's data from API and decode it using the schema.

    Make a request to the API using the given item. Decode the raw JSON
    response into the WarMAC Struct associated with the provided schema.

    :param item: Item to retrieve.
    :param request_schema: Schema to use for decoding the API response.
        Determines the expected structure of the returned data.
    :return: WarMAC Struct corresponding to the request_schema.
    """
    url_partial = SCHEMA_TO_URL[request_schema]
    data_raw = get_page(f"{API_ROOT}{url_partial}{item}", headers=headers).data
    return msgspec.json.decode(data_raw, type=request_schema)


get_data("bite", schema.OrderResponse)
