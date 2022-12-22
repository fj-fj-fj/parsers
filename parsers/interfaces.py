"""The 'interfaces' module contains API."""

__all__ = (
    'AbstractProxy',
    'AbstractRequest',
    'DataStorage',
)
from typing import overload as _overload

from parsers.constants import Constant as _Constant
from parsers.datatypes import ProxyList as _ProxyList
from parsers.datatypes import Json as _Json


class DataStorage:
    """Interface for any storage saving data."""

    STEM = '1_response'
    PARSED_DIR = _Constant.DIR.PARSED_DATA

    @_overload
    def save(self, data: str, mode: str = ...) -> int:
        ...

    @_overload
    def save(self, data: _Json, mode: str = ...) -> int:
        ...

    def save(self, data, mode='w'):
        raise NotImplementedError


class AbstractProxy:
    """Interface for proxy tools."""

    def parse_proxies(self, *args, **kwargs) -> _ProxyList:
        raise NotImplementedError

    def check(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class AbstractRequest:
    """Interface for request tools."""

    def __init__(self) -> None:
        self.proxy = AbstractProxy()

    def get(self):
        raise NotImplementedError
