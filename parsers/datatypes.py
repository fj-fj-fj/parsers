"""The 'datatypes' module contains data structures and types."""
from typing import Protocol as _Protocol
from typing import Type as _Type
from typing import TypeAlias as _TypeAlias
from typing import Union as _Union

from bs4 import BeautifulSoup as _BeautifulSoup

EXIT_CODE = int

# Content of the response, in unicode
HTML: _TypeAlias = str

# Json content of the response, in unicode
JsonStr: _TypeAlias = 'dict[str, "Json"] | list["Json"] | str | int | float | bool | None'

Json: _TypeAlias = dict[str, "Json"] | list["Json"] | str | int | float | bool | None

union_html_json = HTML | Json

ResponseContentStr = _Type[_Union[str, JsonStr]]

union_html_soup_json = str | _BeautifulSoup | Json

ProxyType: _TypeAlias = str
ProxyList: _TypeAlias = list[ProxyType]

TimeoutType: _TypeAlias = _Union[float, tuple[float, float], None]

BS4_PARSER = str | None


class MakeSoupCallable(_Protocol):
    """`BeautifulSoup` callable with variable number of arguments"""

    def __call__(self, *args: HTML | BS4_PARSER) -> _BeautifulSoup:
        ...


class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Sample(list):
    """Container to hodl parsing samples.

    In other words CSS selectors, XPaths, dot-notation-json-keys.
    """

    def __init__(self, *args, file: str = None):
        super().__init__(*args)
        open(file, 'a').close()
        self.file = file

    def save(self, mode='w') -> int:
        with open(self.file, mode) as fh:
            return fh.writelines(f'{line}\n' for line in self)

    def read(self, mode='r') -> list:
        with open(self.file, mode) as fh:
            return [line.strip() for line in fh.readlines()]

    @property
    def wc(self) -> str:
        """Print newline, and byte counts for self.file"""
        with open(self.file) as fh:
            readed = fh.read()
            chars, lines = len(readed), readed.count('\n')
            return f'{chars=} {lines=}'
