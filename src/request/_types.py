"""Module '_types' that contains request types."""
from typing import TypeVar

Proxy = str
ProxyList = list[Proxy]
TimeoutType = TypeVar('TimeoutType', float, tuple[float, float], None)
