from typing import Callable
from typing import Literal

from config import Configuration
from request._types import ProxyList
from request._types import TimeoutType


class AbstractProxy:

    def parse_proxies(
        self,
        cfg: Configuration = Configuration(),
        output: bool = False
    ) -> ProxyList:
        raise NotImplementedError

    def parse(
        self,
        func: Callable = lambda self: self.parse_proxies,
        configs: Configuration = None,
        output: bool = True
    ) -> None:
        raise NotImplementedError

    def check_proxies(
        self,
        frows = -1,
        timeout = True,
        trandom = True,  # random timeout
        file_proxies: str = '',
        file_valid_proxies: str = '',
        file_invalid_proxies: str = '',
        write_mode: Literal['a', 'w'] = 'w',
    ) -> None:
        """Read proxies file (full or frows), sort (valid/invalid files) each."""
        raise NotImplementedError

    def check(
        self,
        proxy: str,
        uagent: str,
        timeout: TimeoutType = None
    ) -> bool:
        """Check proxy and return checked as True/False."""
        raise NotImplementedError


class AbstractRequest:

    def __init__(self) -> None:
        self.proxy = AbstractProxy()

    def get(self):
        raise NotImplementedError
