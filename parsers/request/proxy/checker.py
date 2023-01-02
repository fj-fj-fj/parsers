"""Module 'checker' that contains proxy checkers."""

__all__ = 'check', 'check_proxies'

import typing as _t
import requests as _requests

from parsers.constants import Constant as _Constant
from parsers.request.useragent import gen_useragents_cycle as _gen_useragents_cycle
from parsers.request.times import set_timeout as _set_timeout


_ProxyType: _t.TypeAlias = str


def check(proxy: _ProxyType, uagent: str, timeout=None) -> bool:
    """Check proxy and return availability."""
    try:
        respone = _requests.get(
            url=_Constant.URL.CHECK_PROXY_URL,
            params=dict(_Constant.URL.CHECK_PROXY_URL_PARAMS),
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
    timeout=_set_timeout(),
    file_proxies: str = _Constant.FILE.PARSED_PROXIES,
    file_valid_proxies: str = _Constant.FILE.VALID_PROXIES,
    file_invalid_proxies: str = _Constant.FILE.INVALID_PROXIES,
    write_mode: _t.Literal['a', 'w'] = 'w',  # noqa: F821
) -> None:
    """Sort `file_proxies` to `stop_line` by `file_(valid|invalid)_proxies`."""

    user_agents = _gen_useragents_cycle(file=_Constant.FILE.USER_AGENTS)

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
