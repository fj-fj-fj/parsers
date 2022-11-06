"""This module contains proxy checkers"""

__all__ = 'check', 'check_proxies'

import requests
from typing import Literal, TypeVar

from request.constants import CONSTANTS as const
from request.useragent import gen_useragents_cycle
from utils import set_random_timeout

_Timeout = TypeVar('_Timeout', float, tuple[float, float], None)


def check(proxy: str, uagent: str, timeout: _Timeout = None) -> bool:
    """Request <url> to check proxy"""
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
    frows=-1,
    timeout=True,
    trandom=True,  # random timeout
    file_proxies=const.FILE.PARSED_PROXIES,
    file_valid_proxies=const.FILE.VALID_PROXIES,
    file_invalid_proxies=const.FILE.INVALID_PROXIES,
    write_mode: Literal['a', 'w'] = 'w',
) -> None:
    """Read proxies file (full or frows) and sort (valid/invalid files) each"""

    def set_timeout():
        """Set timeout as floats (default or random) or None"""
        return timeout and set_random_timeout() if trandom else const.TIMEOUT or None  # noqa: E501

    user_agents = gen_useragents_cycle(file=const.FILE.USER_AGENTS)

    with (
        open(file_proxies) as proxies,
        open(file_valid_proxies, write_mode) as valid,
        open(file_invalid_proxies, write_mode) as invalid,
    ):
        for i, proxy in enumerate(proxies.readlines()):
            if i == frows:
                return

            proxy, uagent, timeout = proxy.strip(), next(user_agents), set_timeout()  # noqa: E501
            if check(proxy=proxy, uagent=uagent, timeout=timeout):
                valid.write(proxy + '\n')
            else:
                invalid.write(proxy + '\n')
