__all__ = (
    'AbstractProxy',
    'AbstractRequest',
    'DataStorage',
)
from typing import overload as _overload

from parsers.constants import Constant as _Constant
from parsers.datatypes import Content as _Content
from parsers.datatypes import OpenMode as _OpenMode


class DataStorage:
    """Interface for any storage saving data."""

    PARSED_DIR = _Constant.DIR.PARSED_DATA

    @_overload
    def save(self, data: str, step: int, mode: str = ...) -> int:
        ...

    @_overload
    def save(self, data: _Content.JSON, step: int, mode: str = ...) -> int:
        ...

    def save(self, data, step, mode=_OpenMode.WRITE):
        raise NotImplementedError


class AbstractProxy:
    """Interface for proxy tools."""

    def parse_proxies(self, *args, **kwargs) -> list[str]:
        raise NotImplementedError

    def check(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class AbstractRequest:
    """Interface for request tools."""

    def __init__(self) -> None:
        self.proxy = AbstractProxy()

    def get(self):
        raise NotImplementedError
