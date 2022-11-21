"""Module 'datatypes' that contains data structures and types."""
from typing import Literal
from typing import TypeVar

# config
NamespaceLiteral = Literal['cli', 'file', 'url', 'parse', 'magic_numbers', 'timeouts']

# request
ProxyType = str
ProxyList = list[ProxyType]
TimeoutType = TypeVar('TimeoutType', float, tuple[float, float], None)

# saving data
JsonStr = HTML = str
Data = TypeVar('Data', bytes, HTML, JsonStr, list[str])

# decorators
class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner) -> type:
        return classmethod(self.fget).__get__(None, owner)()
