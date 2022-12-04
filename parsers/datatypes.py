"""The 'datatypes' module contains data structures and types."""
from functools import wraps
from typing import Literal as _Literal
from typing import Type as _Type
from typing import TypeAlias as _TypeAlias
from typing import Union as _Union


# Content of the response, in unicode
HTML: _TypeAlias = str

# Json content of the response, in unicode
JsonStr: _TypeAlias = 'dict[str, "Json"] | list["Json"] | str | int | float | bool | None'

Json: _TypeAlias = dict[str, "Json"] | list["Json"] | str | int | float | bool | None

StrOrJson = HTML | Json

ResponseContentStr = _Type[str | JsonStr]

NamespaceLiteral = _Literal['cli', 'file', 'url', 'parse', 'magic_numbers', 'timeouts']  # noqa: F821

ProxyType: _TypeAlias = str
ProxyList: _TypeAlias = list[ProxyType]

TimeoutType: _TypeAlias = _Union[float, tuple[float, float], None]


class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
