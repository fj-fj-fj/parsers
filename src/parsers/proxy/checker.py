"""Module 'checker' that contains proxy checkers."""

__all__ = 'check', 'check_proxies'

import requests
from typing import Literal

from datatypes import ProxyType
from datatypes import TimeoutType
from constants import ConstantStorage as const
from request.useragent import gen_useragents_cycle
from request.times import set_timeout


def check(proxy: ProxyType, uagent: str, timeout: TimeoutType = None) -> bool:
    """Check proxy and return checked as True/False."""
    try:
        respone = requests.get(
            url=const.URL.CHECK_PROXY_URL,
            params=const.URL.CHECK_PROXY_URL_PARAMS,
            headers={'user-agent': uagent},
            timeout=timeout,
            proxies={'https': 'https://' + proxy},
        )
        print(f'+ {proxy} {respone}')
        return True
    except requests.RequestException as re:
        print(f'- {proxy} {re!r}')
    return False


def check_proxies(
    stop_line: int = -1,
    timeout: TimeoutType = set_timeout(),
    file_proxies: str = const.FILE.PARSED_PROXIES,
    file_valid_proxies: str = const.FILE.VALID_PROXIES,
    file_invalid_proxies: str = const.FILE.INVALID_PROXIES,
    write_mode: Literal['a', 'w'] = 'w',
) -> None:
    """Read proxies file (full or frows), sort (valid/invalid files) each."""

    user_agents = gen_useragents_cycle(file=const.FILE.USER_AGENTS)

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
