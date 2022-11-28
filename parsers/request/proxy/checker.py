"""Module 'checker' that contains proxy checkers."""

__all__ = 'check', 'check_proxies'

import requests as _requests
from typing import Literal as _Literal

from parsers.datatypes import ProxyType as _ProxyType
from parsers.datatypes import TimeoutType as _TimeoutType
from parsers.constants import ConstantStorage as _const
from parsers.request.useragent import gen_useragents_cycle as _gen_useragents_cycle
from parsers.request.times import set_timeout as _set_timeout


def check(proxy: _ProxyType, uagent: str, timeout: _TimeoutType = None) -> bool:
    """Check proxy and return availability."""
    try:
        respone = _requests.get(
            url=_const.URL.CHECK_PROXY_URL,
            params=_const.URL.CHECK_PROXY_URL_PARAMS,
            headers={'user-agent': uagent},
            timeout=timeout,
            proxies={'https': 'https://' + proxy},
        )
        print(f'+ {proxy} {respone}')
        return True
    except _requests.RequestException as re:
        print(f'- {proxy} {re!r}')
    return False


def check_proxies(
    stop_line: int = -1,
    timeout: _TimeoutType = _set_timeout(),
    file_proxies: str = _const.FILE.PARSED_PROXIES,
    file_valid_proxies: str = _const.FILE.VALID_PROXIES,
    file_invalid_proxies: str = _const.FILE.INVALID_PROXIES,
    write_mode: _Literal['a', 'w'] = 'w',  # noqa: F821
) -> None:
    """Sort `file_proxies` to `stop_line` by `file_(valid|invalid)_proxies`."""

    user_agents = _gen_useragents_cycle(file=_const.FILE.USER_AGENTS)

    with (
        open(file_proxies) as proxies,
        open(file_valid_proxies, write_mode) as valid,
        open(file_invalid_proxies, write_mode) as invalid,
    ):
        for line, proxy in enumerate(proxies.readlines()):
            if line == stop_line:
                return

            if check(proxy=proxy.strip(), uagent=next(user_agents), timeout=timeout):
                valid.write(proxy + '\n')
            else:
                invalid.write(proxy + '\n')
