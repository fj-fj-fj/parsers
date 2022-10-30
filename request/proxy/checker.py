"""This module contains proxy checker"""

__all__ = 'check', 'check_proxies'

import requests
from itertools import cycle

from request.proxy.constants import const as px_const
from request.useragent import gen_user_agents
from request.useragent.constants import const as ua_const
from utils import selfcheck_for_interactive_mode


def check(proxy, uagent, timeout=3, rbool=False) -> bool | str:
    """GET `ua_const.CHECK_PROXY_URL` to check proxy"""
    try:
        print(requests.get(ua_const.CHECK_PROXY_URL,
            params=ua_const.CHECK_PROXY_URL_PARAMS,
            headers={'user-agent': uagent},
            timeout=timeout,
            proxies={'https': 'https://' + proxy},
        ))
        success_msg = f'+ {proxy} (ok)'
        return True if rbool else success_msg
    except Exception as e:
        error_msg = f'- {proxy} ({e})'
        return False if rbool else error_msg


def check_proxies(frows=-1, file=px_const.FILE_PARSED_PROXIES, rbool=False):
    """Read proxies file (full or frows) and check each.
    rbool (return bool, not str) is passed to check()
    """
    with open(file) as proxies_file:
        user_agents = cycle(gen_user_agents())
        for i, proxy in enumerate(proxies_file.readlines()):
            if i == frows: return

            proxy, uagent = proxy.strip(), next(user_agents)
            print(check(proxy=proxy, uagent=uagent, rbool=rbool))
