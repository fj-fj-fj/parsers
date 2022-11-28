"""Module 'interfaces'."""
from parsers.datatypes import ProxyList


class DataStorage:
    """Interface for any storage saving data."""

    def save(self, data: str | bytes | list) -> None:
        raise NotImplementedError


class AbstractProxy:
    """Interface for proxy tools."""

    def parse_proxies(self, *args, **kwargs) -> ProxyList:
        raise NotImplementedError

    def check(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class AbstractRequest:
    """Interface for request tools."""

    def __init__(self) -> None:
        self.proxy = AbstractProxy()

    def get(self):
        raise NotImplementedError
