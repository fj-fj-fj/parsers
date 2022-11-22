"""Module 'datatypes' that contains data structures and types."""
from typing import Literal as _Literal
from typing import TypeAlias as _TypeAlias
from typing import Union as _Union

JsonStr: _TypeAlias = str
HTML: _TypeAlias = str
Data: _TypeAlias = bytes | HTML | JsonStr | list[str]

NamespaceLiteral = _Literal['cli', 'file', 'url', 'parse', 'magic_numbers', 'timeouts']  # noqa: F821

ProxyType: _TypeAlias = str
ProxyList: _TypeAlias = list[ProxyType]

# error: Type application has too many types (1 expected)  [misc]
# TimeoutType: _TypeAlias = float | tuple[float, float] | None
TimeoutType: _TypeAlias = _Union[float, tuple[float, float], None]


class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
