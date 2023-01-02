# Keep __all__ in semantic order within each category.
__all__ = (
    # Program exit code
    'EXIT_CODE',
    # Content types
    'HTML',
    'Json',
    'Content',
    # Content handlers
    'MakeSoupCallable',
    'ResponseLike',
    # Files
    'OpenMode',
    # Samples
    'SampleStr',
    'SampleList',
    'OptionalSampleList',
    'Sample',
    # Decorators
    'classproperty',
    # Metaclasses
    'NoSetter',
)

import typing as _t
from enum import StrEnum as _StrEnum

from bs4 import BeautifulSoup as _BeautifulSoup

EXIT_CODE: _t.Final = int

HTML: _t.TypeAlias = str
_Json: _t.TypeAlias = object
Json: _t.TypeAlias = dict[str, _Json] | list[_Json] | str | int | float | bool | None


class NoSetter(type):

    __setattr__ = lambda *_: None  # noqa: E731


@_t.final
class Content(metaclass=NoSetter):
    """Content type container"""
    HTML: _t.TypeAlias = HTML
    JSON: _t.TypeAlias = Json
    UNION_HTML_JSON: _t.TypeAlias = HTML | Json
    UNION_HTML_SOUP_JSON: _t.TypeAlias = HTML | _BeautifulSoup | Json
    UNION_SOUP_JSON: _t.TypeAlias = _BeautifulSoup | Json

    __setattr__ = NoSetter.__setattr__


class MakeSoupCallable(_t.Protocol):

    def __call__(self, *args: tuple[HTML, str | None]) -> _BeautifulSoup:
        ...


class classproperty(property):
    """Property class method"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


@_t.final
class OpenMode(_StrEnum):
    APPEND: _t.Final = 'a'
    BINARY: _t.Final = 'b'
    READ: _t.Final = 'r'
    WRITE: _t.Final = 'w'


SampleStr: _t.TypeAlias = str
SampleList: _t.TypeAlias = list[SampleStr]
OptionalSampleList: _t.TypeAlias = list[SampleStr | None] | None


class Sample(list):
    """Container to hodl parsing samples"""

    def __init__(self, *args: OptionalSampleList, file: str):
        """Init Sample object and touch `file`"""
        super().__init__(*args)
        open(file, 'a').close()
        self.file = file

    def save(self, mode=OpenMode.WRITE, truncate: bool = False) -> int:
        """Save samples or clear `self.file` if `truncate`"""
        with open(self.file, mode) as fh:
            if truncate:
                return 0
            return fh.writelines(f'{line}\n' for line in self)

    def read(self, mode=OpenMode.READ) -> SampleList:
        with open(self.file, mode) as fh:
            return [line.strip() for line in fh.readlines()]

    # GOTO: __add__ (validate selector)

    @_t.final
    @property
    def wc(self) -> str:
        """Print newline, and byte counts for `self.file`"""
        with open(self.file) as fh:
            readed = fh.read()
            chars, lines = len(readed), readed.count('\n')
            return f'{chars=} {lines=}'


class ResponseLike(_t.Protocol):
    """Ojbect with `text` property and `json` method"""

    def json(self) -> Json:
        ...

    @property
    def text(self) -> str:
        ...
