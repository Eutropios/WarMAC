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
import sys

import pytest

from warmac import cli_parser

_EXIT_CODE_ALL_GOOD = 0
_EXIT_CODE_GENERIC_ERROR = 1


class TestIntCastInputBounds:
    @staticmethod
    @pytest.mark.parametrize(
        (
            "input_str",
            "min_bound",
            "max_bound",
            "expected_result",
            "should_raise_error",
        ),
        [
            # --- Successful cases ---
            ("1", 1, 10, 1, False),  # Input == min_bound
            ("5", 1, 10, 5, False),  # Input within bounds
            # --- Error cases (outside value bounds) ---
            ("0", 1, 10, None, True),  # Input < min_bound
            ("11", 1, 10, None, True),  # Input > max_bound
            ("5", 10, 1, None, True),  # min_bound > max_bound
            ("10", 1, 10, None, True),  # Input == max_bound
        ],
        ids=[
            "input_equals_min-bound",
            "input_within_bounds",
            "input_lt_min_error",
            "input_gt_max_error",
            "min_gt_max_error",
            "input_equals_max",
        ],
    )
    def test_str_to_int_bounds_check(
        input_str: str,
        min_bound: int,
        max_bound: int,
        expected_result: int | None,
        *,
        should_raise_error: bool,
    ) -> None:
        """Test str_to_int_bounds_check for edge-case integers wrt
        bounds, asserting either correct conversion or
        ArgumentTypeError."""  # noqa: D205, D209
        if should_raise_error:
            with pytest.raises(argparse.ArgumentTypeError):
                cli_parser.str_to_int_bounds_check(input_str, min_bound, max_bound)
        else:
            actual_output = cli_parser.str_to_int_bounds_check(
                input_str, min_bound, max_bound
            )
            assert actual_output == expected_result


class TestIntCastInputParamTypes:
    @staticmethod
    @pytest.mark.parametrize(
        "invalid_input_string",
        [
            "1.5",  # Input is a float-like string
            "33foobar",  # Input is a mixed string
            "True",  # Input is a boolean-like string
            "None",  # Input is a None-like string
            "invalid",  # General invalid string
            "",  # Empty string
        ],
        ids=[
            "input_float-like_str",
            "input_mixed_str",
            "input_bool-like_str",
            "input_None_str",
            "invalid_str",
            "empty_str",
        ],
    )
    def test_invalid_input_strings_throw_error(
        invalid_input_string: str,
    ) -> None:
        """Test invalid string inputs for str_to_int_bounds_check to
        ensure argparse.ArgumentTypeError is raised."""  # noqa: D205, D209
        min_bound = 1
        max_bound = 10
        with pytest.raises(argparse.ArgumentTypeError):
            cli_parser.str_to_int_bounds_check(
                invalid_input_string, min_bound, max_bound
            )


class TestHandleInputInterface:
    @staticmethod
    @pytest.mark.parametrize(
        ("input_args", "expected_exit_code"),
        [
            # Exit code 1 scenarios
            ([], _EXIT_CODE_GENERIC_ERROR),
            (None, _EXIT_CODE_GENERIC_ERROR),
            (["average"], _EXIT_CODE_GENERIC_ERROR),
            # Exit code 0 scenarios
            (["help"], _EXIT_CODE_ALL_GOOD),
            (["help", "average"], _EXIT_CODE_ALL_GOOD),
            (["--help"], _EXIT_CODE_ALL_GOOD),
        ],
        ids=[
            "no_args_raise_err",
            "None_arg_raise_err",
            "only_subcommand_raise_err",
            "help_subcommand_only",
            "help_with_subcommand",
            "help_flag",
        ],
    )
    def test_cli_exit_codes(
        input_args: list[str] | None, expected_exit_code: int
    ) -> None:
        """Test command-line inputs to ensure correct exit code."""
        with pytest.raises(SystemExit) as excinfo:
            (
                cli_parser.handle_input()
                if input_args is None
                else cli_parser.handle_input(input_args)
            )
        assert excinfo.value.code == expected_exit_code

    @staticmethod
    def test_valid_command_returns_parsed_args() -> None:
        """Test valid command to ensure it returns expected
        argparse.Namespace object."""  # noqa: D205, D209
        parsed_args = cli_parser.handle_input(["average", "bite"])
        assert isinstance(parsed_args, argparse.Namespace)
        assert parsed_args.subparser == "average"
        assert parsed_args.item == "bite"


class TestStdlibMonkeyPatching:
    # these checks need to be done because the internals are being
    # altered and/or inherited from, which is inherently unsafe

    @staticmethod
    def test_positionals_header_is_correct() -> None:
        """Test that argparse subcommand is altered correctly."""
        parser = cli_parser.create_parser()
        expected_title = "commands"
        assert parser._positionals.title == expected_title  # noqa: SLF001

    @staticmethod
    @pytest.mark.parametrize(
        ("terminal_width", "expected_output", "test_subparser"),
        [
            (
                60,
                "usage: usage here\n\nsome description\n\npositional arguments:\n"
                "  stuff       More stuff.\n\noptions:\n  -h, --help  Show this message"
                " and exit.\n",
                False,
            ),  # full-width output
            (
                10,
                "usage: usage here\n\nsome description\n\npositional arguments:\n"
                "  stuff   More stuff.\n\noptions:\n  -h, --help\n          Show this"
                " message and exit.\n",
                False,
            ),  # Intentionally forcing a reformatting for help text
            (
                60,
                "usage: usage here stuff [-h]\n\nStuff description\n\noptions:\n"
                "  -h, --help  Show this message and exit.\n",
                True,
            ),
            (
                10,
                "usage: usage here stuff [-h]\n\nStuff description\n\noptions:\n"
                "  -h, --help\n          Show this message and exit.\n",
                True,
            ),
        ],
        ids=[
            "intended_cli_bare",
            "cramped_cli_bare",
            "intended_cli_subcommand",
            "cramped_cli_subcommand",
        ],
    )
    def test_overridden_help_formatter(
        terminal_width: int, expected_output: str, *, test_subparser: bool
    ) -> None:
        """Test finished output for metavar tuples, poor leading
        indents, and incorrect help text spacing."""  # noqa: D205, D209
        help_min_width = 34
        # Uses mocked terminal_width
        default_width = min(help_min_width, terminal_width)
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
        stuff_parser = subparsers.add_parser(
            "stuff",
            help="More stuff.",
            formatter_class=lambda prog: cli_parser.CustomHelpFormat(
                prog=prog,
                max_help_position=default_width,
            ),
            description="Stuff description",
            add_help=False,
        )
        target_parser = stuff_parser if test_subparser else some_parser

        # Add the help argument to the chosen parser
        target_parser.add_argument(
            "-h", "--help", action="help", help="Show this message and exit."
        )

        # Assert the formatted help output matches the expected output
        assert target_parser.format_help() == expected_output


if __name__ == "__main__":
    sys.exit(pytest.main())
