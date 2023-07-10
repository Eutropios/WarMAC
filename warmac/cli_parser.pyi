import argparse as ap
from collections.abc import Callable as Callable
from collections.abc import Generator

_AVG_FUNCS: tuple[str, str, str, str, str, str]
DEFAULT_TIME: int
_DESCRIPTION: str
_HELP_MIN_WIDTH: int
_DEFAULT_WIDTH: int
_MAX_TIME_RANGE: int
_PLATFORMS: tuple[str, str, str, str]
_PROG_NAME: str
_RELIC_REFINEMENTS: tuple[str, str, str, str]
VERSION: str

class CustomHelpFormat(ap.RawDescriptionHelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = ...,
        max_help_position: int = ...,
        width: int | None = ...,
    ) -> None: ...
    def _format_action_invocation(self, action: ap.Action) -> str: ...
    def _format_action(self, action: ap.Action) -> str: ...
    def _iter_indented_subactions(
        self, action: ap.Action
    ) -> Generator[ap.Action, None, None]: ...

def _int_checking(user_int: str, upper_bound: int) -> int | None: ...
def _create_parser() -> ap.ArgumentParser: ...
def handle_input() -> ap.Namespace: ...
