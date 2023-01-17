__all__ = (
    'Colors',
    'remove_escape_sequences',
)

import re as _re
from enum import StrEnum as _StrEnum


class Colors(_StrEnum):
    ESC = '\x1B['
    BLUE = f'{ESC}0;36m'
    RED = f'{ESC}31m'
    YELLOW = f'{ESC}33m'
    NC = f'{ESC}0m'


def remove_escape_sequences(string) -> str:
    """Remove the 7-bit C1 ANSI escape sequences from a `string`"""
    ansi_escape = _re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', _re.VERBOSE)
    cleaned = ansi_escape.sub('', string)
    return cleaned
