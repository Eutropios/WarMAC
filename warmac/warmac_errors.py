"""
warmac.warmac_errors
~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the classes used throughout WarMAC.
For information on the main program, please see __init__.py

Date of Creation: June 21, 2023
"""  # noqa: D205,D400

from __future__ import annotations


class WarMACBaseError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self, msg: str = "WarMAC Error.") -> None:
        """
        Construct a ``WarMAC`` exception.

        :param msg: The exception's message, defaults to the phrase
            "WarMAC Error".
        """
        self.message = msg
        super().__init__(self.message)


class SubcommandError(WarMACBaseError):
    """
    Thrown if subparser does not exist in :data:`warmac.SUBCMD_TO_FUNC`.

    Thrown if the ``subparser`` field of ``argparse.Namespace`` does not
    exist within the global dictionary :data:`warmac.SUBCMD_TO_FUNC`.
    """

    def __init__(self) -> None:
        """Construct a ``SubcommandError`` exception."""
        super().__init__("Not a valid subcommand.")


class NoListingsFoundError(WarMACBaseError):
    """
    Thrown if no listings were found.

    Thrown if no order listings are found given the set of parameters
    that the user gives the program.
    """

    def __init__(self) -> None:
        """Construct a ``NoListingsFoundError`` exception."""
        super().__init__("There are no listings matching your search parameters.")


# ---- HTTP Response Code Errors ----


class WarMACHTTPError(WarMACBaseError):
    """
    Thrown if the request experienced an error or gave a bad response.

    Thrown if the request made by the user returned an HTTP Status code
    that was not 200.
    """

    def __init__(self, message: str) -> None:
        """Construct a ``WarMACHTTPError`` exception."""
        super().__init__(message)


class InternalServerError(WarMACHTTPError):
    """
    Thrown if the server has encountered an internal error.

    Thrown on HTTP status code 500, which indicates that the server has
    encountered an internal error that prevents it from fulfilling the
    user's request.
    """

    def __init__(self) -> None:
        """Construct a ``MalformedURLError`` exception."""
        super().__init__(
            "Error 500, warframe.market servers have encountered an internal error "
            "while processing this request.",
        )


class MethodNotAllowedError(WarMACHTTPError):
    """
    Thrown if the target resource doesn't support the desired method.

    Thrown on HTTP status code 405, which indicates that the server
    knows the method, but the target resource doesn't support it.
    """

    def __init__(self) -> None:
        """Construct a ``MethodNotAllowedError`` exception."""
        super().__init__(
            "Error 405, the target resource does not support this function.",
        )


class MalformedURLError(WarMACHTTPError):
    """
    Thrown if the given item does not exist.

    Thrown on HTTP status code 404, which indicates that the resource in
    question does not exist.
    """

    def __init__(self) -> None:
        """Construct a ``MalformedURLError`` exception."""
        super().__init__(
            "This item does not exist. Please check your spelling, and remember to use "
            "quotations if the item is multiple words.",
        )


class ForbiddenRequestError(WarMACHTTPError):
    """
    Thrown if the server refuses to authorize a request.

    Thrown on HTTP status code 403, which indicates that access to the
    desired resource is forbidden.
    """

    def __init__(self) -> None:
        """Construct a ``ForbiddenRequestError`` exception."""
        super().__init__(
            "Error 403, the URL you've requested is forbidden. You do not have"
            " authorization to access it.",
        )


class UnauthorizedAccessError(WarMACHTTPError):
    """
    Thrown if the user doesn't have the correct credentials.

    Thrown on HTTP status code 401, which indicates that authorization
    via proper user credentials is needed to access this resource.
    """

    def __init__(self) -> None:
        """Construct a ``ForbiddenRequestError`` exception."""
        super().__init__(
            "Error 401, insufficient credentials. Please log in to before making this "
            "transaction.",
        )


class UnknownError(WarMACHTTPError):
    """
    Thrown if the HTTP Response Code is not covered.

    Thrown if the HTTP Response Code is not covered by any other error
    previously stated.
    """

    def __init__(self, status_code: int) -> None:
        """Construct an ``UnknownError`` exception."""
        super().__init__(
            f"Unknown Error; HTTP Code {status_code}. Please open a new issue on the "
            "Github page (link in README.md file).",
        )
