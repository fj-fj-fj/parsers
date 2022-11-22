"""Module 'datatypes' that contains data structures and types."""
from typing import Literal
from typing import TypeAlias

# config
NamespaceLiteral = Literal['cli', 'file', 'url', 'parse', 'magic_numbers', 'timeouts']

# request
ProxyType = str
ProxyList = list[ProxyType]
TimeoutType: TypeAlias = float | tuple[float, ...] | None

# saving data
JsonStr: TypeAlias = str
HTML: TypeAlias = str
Data: TypeAlias = bytes | HTML | JsonStr | list[str]

# decorators
class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
