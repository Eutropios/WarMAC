"""
warmac.warmac_errors
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the classes used throughout WarMAC.
For information on the main program, please see main.py

Date of Creation: June 21, 2023
"""  # noqa: D205,D400

VERSION = "0.0.1"
PROG_NAME = "warmac"
DESCRIPTION = "A program to fetch the average market cost of an item in Warframe."


class WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self, message: str = "WarMAC Error.") -> None:
        """
        Construct a WarMAC exception.

        :param message: The message to be printed with the exception;
        defaults to WarMAC Error.
        :type message: str, optional
        """
        self.message = message
        super().__init__(self.message)


class SubcommandError(WarMACError):
    """
    Thrown if subparser field of argparse.Namespace does not exist
    in SUBCOMMANDS.
    """  # noqa: D205

    def __init__(self) -> None:
        """Construct a SubcommandError exception."""
        super().__init__("Not a valid subcommand.")


class StatisticTypeError(WarMACError):
    """Thrown if statistic parameter does not exist in AVG_FUNCS."""

    def __init__(self) -> None:
        """Construct a StatisticTypeError exception."""
        super().__init__("Not a valid statistic type.")


class NoListingsFoundError(WarMACError):
    """Thrown if no listings were found."""

    def __init__(self) -> None:
        """Construct a NoListingsFoundError."""
        super().__init__("There are no listings matching your search parameters.")


class EmptyListProvidedError(WarMACError):
    """Thrown if plat_list is empty in verbose_output."""

    def __init__(self) -> None:
        """Construct an EmptyListFoundError."""
        super().__init__("plat_list cannot be empty.")


# ---- HTTP Response Code Errors ----


class InternalServerError(WarMACError):
    """
    Thrown if the server has encountered an internal error.

    Thrown on HTTP status code 500, which indicates that server has
    encountered an internal error that prevents it from fulfilling
    the user's request.
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

    Thrown on HTTP status code 404, which indicates that the
    resource in question does not exist.
    """

    def __init__(self) -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 404, this item does not exist. Please check your spelling, and "
            "remember to use quotations if the item is multiple words.",
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
    """Thrown if the HTTP Response Code not covered."""

    def __init__(self, status_code: int) -> None:
        """Construct a UnknownError exception."""
        super().__init__(
            f"Unknown Error; HTTP Code {status_code}. Please open a new issue on the "
            "Github page (link in README.md file).",
        )
