"""
tests.test_cli_parser
~~~~~~~~~~~~~~~~~

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

Test file for main.py
"""  # noqa: D205, D400

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

from warmac import average, cli_parser, errors, main

if TYPE_CHECKING:
    from typing import Literal
    from unittest.mock import Mock


class TestFixHttpHeaders:
    @staticmethod
    def test_default_values() -> None:
        """Test that default values are assigned to dictionary."""
        headers: dict[str, str] = {}
        main.fix_http_headers(headers)
        assert headers["Platform"] == "pc"
        assert headers["Crossplay"] == "true"

    @staticmethod
    @pytest.mark.parametrize(
        ("platform", "crossplay", "expected_platform", "expected_crossplay"),
        [
            pytest.param("ps4", True, "ps4", "true", id="ps4_crossplay_true"),
            pytest.param("xbox", False, "xbox", "false", id="xbox_crossplay_false"),
            pytest.param("switch", True, "switch", "true", id="switch_crossplay_true"),
            pytest.param(
                "mobile", False, "mobile", "false", id="mobile_crossplay_false"
            ),
            pytest.param("pc", False, "pc", "false", id="pc_crossplay_false"),
        ],
    )
    def test_various_platform_and_crossplay_combinations(
        platform: Literal["pc", "ps4", "xbox", "switch", "mobile"],
        expected_platform: str,
        expected_crossplay: str,
        mock_http_headers: dict[str, str],
        *,
        crossplay: bool,
    ) -> None:
        """Test different combinations of platform and crossplay."""
        main.fix_http_headers(mock_http_headers, platform=platform, crossplay=crossplay)
        assert mock_http_headers["Platform"] == expected_platform
        assert mock_http_headers["Crossplay"] == expected_crossplay


class TestProcessCliCommand:
    @staticmethod
    @pytest.fixture
    def mock_dependencies(
        mocker: Mock,
    ) -> tuple[MagicMock, MagicMock, datetime.datetime]:
        """Fixture that mocks cli_parser and average.process_data to
        avoid making any HTTP requests."""  # noqa: D205, D209
        mock_cli_args = MagicMock()
        mock_cli_args.subparser = "average"
        mock_cli_args.platform = "ps4"
        mock_cli_args.crossplay = False

        # Forcing the function to return this specific value
        mocker.patch.object(cli_parser, "handle_input", return_value=mock_cli_args)

        # Skip average.process_data
        mock_subcommand_handler = mocker.patch.object(
            average, "process_data", return_value="mocked output data"
        )

        # We're defining our own dictionary here because mock gets pissy
        mock_dispatch = {"average": mock_subcommand_handler}
        mocker.patch("warmac.main.SUBCMD_DISPATCH", new=mock_dispatch)

        mock_datetime_module = mocker.patch("warmac.main.datetime")
        fixed_time = datetime.datetime(
            2024, 7, 25, 12, 0, 0, tzinfo=datetime.timezone.utc
        )
        mock_datetime_module.datetime.now.return_value = fixed_time

        return mock_cli_args, mock_subcommand_handler, fixed_time

    @staticmethod
    def test_process_cli_command_success(
        mock_dependencies: tuple[MagicMock, MagicMock, datetime.datetime],
    ) -> None:
        """Test the successful execution of ``process_cli_command``."""
        mock_cli_args, mock_subcommand_handler, fixed_time = mock_dependencies
        expected_headers = {
            "Accept": "application/json",
            "Accept-Language": "en",
            "Platform": "ps4",
            "Crossplay": "false",
        }

        result = main.process_cli_command(args=["average", "-p", "ps4", "-S"])

        # Assert that the handler was actually called like we wanted
        mock_subcommand_handler.assert_called_once_with(
            mock_cli_args, expected_headers, fixed_time
        )

        assert result == "mocked output data"

    @staticmethod
    def test_process_cli_command_invalid_subcommand(mocker: Mock) -> None:
        """Test that KeyError is raised when an invalid subcommand is
        given to dictionary."""  # noqa: D205, D209
        mock_cli_args = MagicMock()
        mock_cli_args.subparser = "nonexistent_subcommand"
        mocker.patch.object(cli_parser, "handle_input", return_value=mock_cli_args)
        with pytest.raises(KeyError):
            main.process_cli_command(args=["nonexistent_subcommand"])


class TestMain:
    @staticmethod
    def test_main_success(mocker: Mock, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that main returns 0 and prints to stdout on success."""
        mock_process_cli_command = mocker.patch(
            "warmac.main.process_cli_command", return_value="Success message"
        )
        result = main.main(["some", "args"])
        captured = capsys.readouterr()
        assert result == 0
        assert "Success message" in captured.out
        assert not captured.err
        mock_process_cli_command.assert_called_once_with(["some", "args"])

    @staticmethod
    def test_main_warmac_base_error(
        mocker: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that main returns 1 and prints the error to stderr when
        a WarMACBaseError is raised."""  # noqa: D205, D209
        mock_process_cli_command = mocker.patch(
            "warmac.main.process_cli_command",
            side_effect=errors.WarMACBaseError("An error occurred"),
        )
        result = main.main(["some", "args"])
        captured = capsys.readouterr()
        assert result == 1
        assert "An error occurred" in captured.err
        assert not captured.out
        mock_process_cli_command.assert_called_once_with(["some", "args"])

    @staticmethod
    def test_main_key_error_raises_command_error(mocker: Mock) -> None:
        """Test that main re-raises a KeyError as a CommandError."""
        mocker.patch(
            "warmac.main.process_cli_command",
            side_effect=KeyError,
        )
        with pytest.raises(errors.CommandError, match=r"Not a valid command\."):
            main.main(["some", "args"])
