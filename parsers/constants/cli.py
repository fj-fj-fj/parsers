__all__ = [
    'CLI',
    'PARSE',
    'VERBOSE',
]
import typing as _t

PARSE: _t.Final = '--parse'
VERBOSE: _t.Final = '--verbose'

class CLI(_t.NamedTuple):
    PARSE: str = PARSE
    VERBOSE: str = VERBOSE
