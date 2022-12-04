"""The 'interfaces' module contains API."""

__all__ = (
    'AbstractProxy',
    'AbstractRequest',
    'DataStorage',
)

from parsers.constants import ConstantStorage as _ConstantStorage
from parsers.datatypes import ProxyList as _ProxyList


class DataStorage:
    """Interface for any storage saving data."""

    PARSED_DIR = _ConstantStorage.FILE.PARSED_DATA

    def save(self, data: str | bytes | list) -> None:
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
