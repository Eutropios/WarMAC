"""
Errors used within warmac.

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


class WarMACBaseError(Exception):
    """Base error raised in WarMAC."""

    def __init__(self, msg: str = "WarMAC Error.") -> None:
        """
        Construct a ``WarMACBaseError``.

        :param msg: Error's message, defaults to the phrase "WarMAC
            Error."
        """
        self.message = msg
        super().__init__(self.message)


class CommandError(WarMACBaseError):
    """Raised if the ``subparser`` field of ``argparse.Namespace`` does
    not exist in :py:data:`main.SUBCMD_DISPATCH`."""

    def __init__(self) -> None:
        """Construct a ``CommandError``."""
        super().__init__("Not a valid command.")


class NoListingsFoundError(WarMACBaseError):
    """Raised if no order listings are found given the set of parameters
    that the user gives the program."""

    def __init__(self) -> None:
        """Construct a ``NoListingsFoundError``."""
        super().__init__("There are no listings matching your search parameters.")


# ---- HTTP Response Code Errors ----


class WarMACHTTPError(WarMACBaseError):
    """Raised if the request made by the user returned an HTTP Status
    code that was not 200."""

    def __init__(self, message: str) -> None:
        """Construct a ``WarMACHTTPError`` error."""
        super().__init__(message)


class InternalServerError(WarMACHTTPError):
    """Raised on HTTP status code 500, which indicates that the server
    has encountered an internal error that prevents it from fulfilling
    the user's request."""

    def __init__(self) -> None:
        """Construct an ``InternalServerError``."""
        super().__init__(
            "Error 500: warframe.market servers have encountered an internal error "
            "while processing this request.",
        )


class RateLimitError(WarMACHTTPError):
    """Raised on HTTP status code 429, which indicates that the an
    excessive number of requests per second have been made to the WFM
    server."""

    def __init__(self) -> None:
        """Construct a ``RateLimitError``."""
        super().__init__(
            "You have exceeded Warframe Market's allotted requests per second, the "
            "current limit being 3 per second. Please wait a few moments before making "
            "additional requests. For more information, please read "
            "the documentation.",
        )


class MethodNotAllowedError(WarMACHTTPError):
    """Raised on HTTP status code 405, which indicates that the server
    knows the method, but the target resource doesn't support it."""

    def __init__(self) -> None:
        """Construct a ``MethodNotAllowedError``."""
        super().__init__(
            "Error 405: The target resource does not support this function.",
        )


class MalformedURLError(WarMACHTTPError):
    """Raised on HTTP status code 404, which indicates that the resource
    in question does not exist."""

    def __init__(self) -> None:
        """Construct a ``MalformedURLError``."""
        super().__init__(
            "This item does not exist on Warframe Market. Please check your spelling "
            "and remember to use quotations if the item is multiple words.",
        )


class ForbiddenRequestError(WarMACHTTPError):
    """Raised on HTTP status code 403, which indicates that access to
    the desired resource is forbidden."""

    def __init__(self) -> None:
        """Construct a ``ForbiddenRequestError``."""
        super().__init__(
            "Error 403: The URL you've requested is forbidden. You do not have"
            " authorization to access it.",
        )


class UnauthorizedAccessError(WarMACHTTPError):
    """Raised on HTTP status code 401, which indicates that
    authorization via proper user credentials is needed to access this
    resource."""

    def __init__(self) -> None:
        """Construct an ``UnauthorizedAccessError``."""
        super().__init__(
            "Error 401: Insufficient credentials. Please log in to before making this "
            "transaction.",
        )


class UnknownError(WarMACHTTPError):
    """Raised if the HTTP Response Code is not covered by any other
    error previously stated."""

    def __init__(self, status_code: int) -> None:
        """Construct an ``UnknownError``."""
        super().__init__(
            f"Unknown Error - HTTP Code {status_code}: Please open a new issue on the "
            "GitHub page (link in README.md file).",
        )
