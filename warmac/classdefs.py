"""
warmac.classdefs
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the classes used throughout WarMAC.
For information on the main program, please see main.py

Date of Creation: June 21, 2023
Date Last Modified: June 21, 2023
Version of Python required for module: >=3.6.0
"""  # noqa: D205,D400

VERSION = "1.5.8"  # defining the version of the program, used across WarMAC


class WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self: "WarMACError", message: str = "WarMAC Error.") -> None:
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

    def __init__(self: "SubcommandError") -> None:
        """Construct a SubcommandError exception."""
        super().__init__("Not a valid subcommand.")


class InternalServerError(WarMACError):
    """
    Thrown if the server has encountered an internal error.

    Thrown on HTTP status code 500, which indicates that server has
    encountered an internal error that prevents it from fulfilling
    the user's request.
    """

    def __init__(self: "InternalServerError") -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 500, Warframe.market servers have encountered an "
            "internal error while processing this request."
        )


class MethodNotAllowedError(WarMACError):
    """
    Thrown if the target resource doesn't support the desired method.

    Thrown on HTTP status code 405, which indicates that the server
    knows the method, but the target resource doesn't support it.
    """

    def __init__(self: "MethodNotAllowedError") -> None:
        """Construct a MethodNotAllowedError exception."""
        super().__init__(
            "Error 405, the target resource does not support this function."
        )


class MalformedURLError(WarMACError):
    """
    Thrown if there the item name given to WarMAC doesn't exist.

    Thrown on HTTP status code 404, which indicates that the
    resource in question does not exist.
    """

    def __init__(self: "MalformedURLError") -> None:
        """Construct a MalformedURLError exception."""
        super().__init__(
            "Error 404, this item does not exist. Please check your spelling, and "
            "remember to use quotations if the item is multiple words."
        )


class ForbiddenRequestError(WarMACError):
    """
    Thrown if the server refuses to authorize a request.

    Thrown on HTTP status code 403, which indicates that access to the
    desired resources is forbidden.
    """

    def __init__(self: "ForbiddenRequestError") -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 403, the URL you've requested is forbidden. You do not have"
            " authorization to access it."
        )


class UnauthorizedAccessError(WarMACError):
    """
    Thrown if the user doesn't have the correct credentials.

    Thrown on HTTP status code 401, which indicates that authorization
    via proper user credentials is needed to access this resource.
    """

    def __init__(self: "UnauthorizedAccessError") -> None:
        """Construct a ForbiddenRequestError exception."""
        super().__init__(
            "Error 401, insufficient credentials. Please log in to access this content."
        )


class UnknownError(WarMACError):
    """Thrown if the error is unknown."""

    def __init__(self: "UnknownError", status_code: int) -> None:
        """Construct a UnknownError exception."""
        super().__init__(
            f"Unknown Error; HTTP Code {status_code}. Writing to errorLog.txt file."
            " Please open a new issue on the Github page (link in README.rst file)."
        )
