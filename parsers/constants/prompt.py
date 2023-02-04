__all__ = [
    'ENTER_BS4_PARSER',
    'ENTER_URL_OR_FALSE',
    'Prompt',
]
import typing as _t

ENTER_BS4_PARSER = "Enter markup parser (default: 'lxml'):  "
ENTER_URL_OR_FALSE = "Enter URL (default: 'httpbin.org'): "

class Prompt(_t.NamedTuple):
    ENTER_BS4_PARSER: str = ENTER_BS4_PARSER
    ENTER_URL_OR_FALSE: str = ENTER_URL_OR_FALSE
