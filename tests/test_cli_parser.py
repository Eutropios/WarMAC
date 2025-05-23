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

import argparse
import shutil
import sys

import pytest

from warmac import cli_parser

_EXIT_CODE_ALL_GOOD = 0
_EXIT_CODE_GENERIC_ERROR = 1
_EXIT_CODE_SHELL_BUILTIN_ERROR = 2


class TestIntCastInterface:
    # Valid params
    @staticmethod
    def test_input_cast_to_int_with_valid_params() -> None:
        expected_output = 5
        assert cli_parser.str_to_int_bounds_check("5", 1, 10) == expected_output

    # min > max
    @staticmethod
    def test_min_greater_than_max_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("5", 10, 1)


class TestIntCastInputBounds:
    # Input == min
    @staticmethod
    def test_input_val_equal_to_min_val() -> None:
        expected_output = 1
        assert cli_parser.str_to_int_bounds_check("1", 1, 10) == expected_output

    # Input < min
    @staticmethod
    def test_below_min_value_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("0", 1, 10)

    # Input == max
    @staticmethod
    def test_input_val_equal_to_max_val_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("10", 1, 10)

    # Input > max
    @staticmethod
    def test_above_max_value_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("11", 1, 10)


class TestIntCastInputParamTypes:
    # Input is a float
    @staticmethod
    def test_float_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("1.5", 1, 10)

    # Input is a mixed string
    @staticmethod
    def test_mixed_string_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("33foobar", 1, 10)

    # Input is a boolean
    @staticmethod
    def test_boolean_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("True", 1, 10)

    # Input is None
    @staticmethod
    def test_none_input_throws_error() -> None:
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check("None", 1, 10)


class TestHandleInputInterface:
    # exit code 1 when "warmac" is called
    @staticmethod
    def test_bare_command_with_empty_list_exit_code_one() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input([])
        assert exit_code.value.code == _EXIT_CODE_GENERIC_ERROR

    # exit code 1 when "warmac" is called, dupe from above
    @staticmethod
    def test_bare_command__with_none_input_exit_code_one() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input()
        assert exit_code.value.code == _EXIT_CODE_GENERIC_ERROR

    # exit code 1 when "warmac average" is called
    @staticmethod
    def test_bare_average_command_exit_code_one() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input(["average"])
        assert exit_code.value.code == _EXIT_CODE_GENERIC_ERROR

    # exit code 0 when "warmac help" is called
    @staticmethod
    def test_bare_help_command_exit_code_zero() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input(["help"])
        assert exit_code.value.code == _EXIT_CODE_ALL_GOOD

    # exit code 0 when "warmac help average" is called
    @staticmethod
    def test_help_with_arg_exit_code_zero() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input(["help", "average"])
        assert exit_code.value.code == _EXIT_CODE_ALL_GOOD

    # exit code 0 when "warmac --help" is called
    @staticmethod
    def test_bare_command_with_help_option_exit_code_zero() -> None:
        with pytest.raises(SystemExit) as exit_code:
            cli_parser.handle_input(["--help"])
        assert exit_code.value.code == _EXIT_CODE_ALL_GOOD

    # valid parsed content
    @staticmethod
    def test_valid_command_returns_parsed_args() -> None:
        parsed_args = cli_parser.handle_input(["average", "bite"])
        assert parsed_args.subparser == "average"
        assert parsed_args.item == "bite"


class TestStdlibMonkeyPatching:
    # these checks need to be done because the internals are being
    # altered and/or inherited from, which is inherently unsafe

    # argparse subcommand title is correct
    @staticmethod
    def test_positionals_header_is_correct() -> None:
        parser = cli_parser.create_parser()
        expected_title = "commands"
        assert parser._positionals.title == expected_title  # noqa: SLF001

    # overridden methods of subclass are formatted correctly
    @staticmethod
    def test_overridden_help_formatter() -> None:
        help_min_width = 34
        default_width = min(help_min_width, shutil.get_terminal_size().columns - 2)
        some_parser = cli_parser.WarMACParser(
            prog="progname",
            usage="usage here",
            description="some description",
            formatter_class=lambda prog: cli_parser.CustomHelpFormat(
                prog=prog,
                max_help_position=default_width,
            ),
            add_help=False,
        )

        subparsers = some_parser.add_subparsers(dest="subparser", metavar="")
        subparsers.add_parser(
            "stuff",
            help="More stuff.",
            formatter_class=lambda prog: cli_parser.CustomHelpFormat(
                prog=prog,
                max_help_position=default_width,
            ),
            add_help=False,
        )

        some_parser.add_argument(
            "-h",
            "--help",
            action="help",
            help="Show this message and exit.",
        )
        some_help = some_parser.format_help()
        assert (
            some_help
            == "usage: usage here\n\nsome description\n\npositional arguments:\n"
            "  stuff       More stuff.\n\noptions:\n  -h, --help  Show this message"
            " and exit.\n"
        )


if __name__ == "__main__":
    sys.exit(pytest.main())
