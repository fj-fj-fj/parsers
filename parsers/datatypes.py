"""The 'datatypes' module contains data structures and types."""
from typing import Protocol as _Protocol
from typing import Type as _Type
from typing import TypeAlias as _TypeAlias
from typing import Union as _Union

from bs4 import BeautifulSoup as _BeautifulSoup


# Content of the response, in unicode
HTML: _TypeAlias = str

# Json content of the response, in unicode
JsonStr: _TypeAlias = 'dict[str, "Json"] | list["Json"] | str | int | float | bool | None'

Json: _TypeAlias = dict[str, "Json"] | list["Json"] | str | int | float | bool | None

StrOrJson = HTML | Json

ResponseContentStr = _Type[_Union[str, JsonStr]]

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
