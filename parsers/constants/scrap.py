__all__ = [
    'BUILTIN',
    'FASTEST',
    'HTML_PARSER',
    'HTML5LIB',
    'LXML',
    'MarkupParser',
    'Scrap',
]
import typing as _t

HTML_PARSER: _t.Final = 'html.parser'
LXML: _t.Final = 'lxml'  # pip install
HTML5LIB: _t.Final = 'html5lib'  # pip install

BUILTIN: _t.Final = HTML_PARSER
FASTEST = LXML


class MarkupParser(_t.NamedTuple):
    """
    HTML_PARSER = 'html.parser'
        https://docs.python.org/3/library/html.parser.html
    LXML = 'lxml'
        https://github.com/html5lib/html5lib-python
    HTML5LIB = 'html5lib'
        https://github.com/lxml/lxml

    """
    HTML_PARSER: str = HTML_PARSER
    HTML5LIB: str = HTML5LIB
    LXML: str = LXML

    BUILTIN: str = HTML_PARSER
    FASTEST: str = LXML


class Scrap(_t.NamedTuple):
    PARSERS: MarkupParser = MarkupParser()
    PARSER: str = PARSERS.BUILTIN
