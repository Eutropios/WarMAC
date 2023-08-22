"""
warmac.warmac_errors
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the classes used throughout WarMAC.
For information on the main program, please see main.py

Date of Creation: June 21, 2023
"""  # noqa: D205,D400

from __future__ import annotations

VERSION = "0.0.3"
PROG_NAME = "warmac"
DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."


class WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self, msg: str = "WarMAC Error.") -> None:
        """
        Construct a WarMAC exception.

        :param msg: The exception's message, defaults to "WarMAC Error".
        :type msg: str, optional
        """
        self.message = msg
        super().__init__(self.message)


class SubcommandError(WarMACError):
    """
    Thrown if subparser does not exist in SUBCOMMANDS.

    Thrown if the subparser field of argparse.Namespace does not exist
    within the global dictionary SUBCOMMANDS.
    """

    def __init__(self) -> None:
        """Construct a SubcommandError exception."""
        super().__init__("Not a valid subcommand.")


class StatisticTypeError(WarMACError):
    """
    Thrown if statistic parameter does not exist in AVG_FUNCS.

    Thrown if the statistic field of argparse.Namespace does not exist
    within the global dictionary AVG_FUNCS.
    """

    def __init__(self) -> None:
        """Construct a StatisticTypeError exception."""
        super().__init__("Not a valid statistic type.")


class NoListingsFoundError(WarMACError):
    """
    Thrown if no listings were found.

    Thrown if no order listings are found given the set of parameters
    that the user gives the program.
    """

    def __init__(self) -> None:
        """Construct a NoListingsFoundError."""
        super().__init__("There are no listings matching your search parameters.")


# ---- HTTP Response Code Errors ----


class InternalServerError(WarMACError):
    """
    Thrown if the server has encountered an internal error.

    Thrown on HTTP status code 500, which indicates that server has
    encountered an internal error that prevents it from fulfilling the
    user's request.
    """

    def __init__(self) -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 500, Warframe.market servers have encountered an "
            "internal error while processing this request.",
        )


class MethodNotAllowedError(WarMACError):
    """
    Thrown if the target resource doesn't support the desired method.

    Thrown on HTTP status code 405, which indicates that the server
    knows the method, but the target resource doesn't support it.
    """

    def __init__(self) -> None:
        """Construct a MethodNotAllowedError exception."""
        super().__init__(
            "Error 405, the target resource does not support this function.",
        )


class MalformedURLError(WarMACError):
    """
    Thrown if there the item name given to WarMAC doesn't exist.

    Thrown on HTTP status code 404, which indicates that the resource in
    question does not exist.
    """

    def __init__(self) -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "This item does not exist. Please check your spelling, and remember to use "
            "quotations if the item is multiple words.",
        )


class ForbiddenRequestError(WarMACError):
    """
    Thrown if the server refuses to authorize a request.

    Thrown on HTTP status code 403, which indicates that access to the
    desired resources is forbidden.
    """

    def __init__(self) -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 403, the URL you've requested is forbidden. You do not have"
            " authorization to access it.",
        )


class UnauthorizedAccessError(WarMACError):
    """
    Thrown if the user doesn't have the correct credentials.

    Thrown on HTTP status code 401, which indicates that authorization
    via proper user credentials is needed to access this resource.
    """

    def __init__(self) -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 401, insufficient credentials. Please log in to before making this "
            "transaction.",
        )


class UnknownError(WarMACError):
    """
    Thrown if the HTTP Response Code is not covered.

    Thrown if the HTTP Response Code is not covered by any other error
    previously stated.
    """

    def __init__(self, status_code: int) -> None:
        """Construct a UnknownError exception."""
        super().__init__(
            f"Unknown Error; HTTP Code {status_code}. Please open a new issue on the "
            "Github page (link in README.md file).",
        )
