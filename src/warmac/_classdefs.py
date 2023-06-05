"""
warmac._classdefs
~~~~~~~~~~~~~~~~~

Copyright (c) 2023 Noah Jenner under MIT License
Please see LICENSE.txt for additional licensing information.

File that contains the classes used throughout WarMAC.
For information on the main program, please see main.py

Date of Creation: May 27, 2023
Date Last Modified: June 4, 2023
Version of Python required for module: >=3.0.0
"""  # noqa: D205,D400

VERSION = "1.5.8"  # defining the version of the program, used across WarMAC


class WarMACError(Exception):
    """Base exception thrown in WarMAC."""

    def __init__(self, message: str = "WarMAC Error.") -> None:
        """Construct a WarMAC exception.

        :param message: The message to be printed with the exception; defaults to
        'WarMAC Error.'
        :type message: str, optional
        """
        self.message = message
        super().__init__(self.message)


class AverageTypeError(WarMACError):
    """Thrown if average type given is not mean, median, mode, or harmonic."""

    def __init__(self) -> None:
        """Construct a _AverageTypeError exception."""
        super().__init__("Not an acceptable average type.")


class MalformedURLError(WarMACError):
    """Thrown if there the item name given to WarMAC doesn't exist."""

    def __init__(self) -> None:
        """Construct a _MalformedURLError exception."""
        super().__init__(
            "This item does not exist. Please check your spelling, and remember to use"
            " parenthesis in the command line if the item is multiple words."
        )


class UnknownError(WarMACError):
    """Thrown if the error is unknown."""

    def __init__(self) -> None:
        """Construct a UnknownError exception."""
        super().__init__(
            "Unknown error, writing to errorLog.txt file. Please open a new issue on "
            "the Github page (link in README.rst file)."
        )
