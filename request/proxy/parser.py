"""Proxy parsing module"""
# This module cannot be running.
# To get proxies manually use ../__init__.py with -i

__all__ = 'parse', 'parse_proxies'

import requests
from bs4 import BeautifulSoup

from proxy.constants import const
from utils import save


def parse(**kw):
    """Parse proxies with print parsed"""
    response = parse_proxies(log=True, **kw)
    return f'{response=}'


def parse_proxies(log=False, **kw) -> list:
    """Parse proxies from `constants.const.URL`"""
    url, fpx, fresp, parser = set_default(**kw).values()

    response = requests.get(url).text
    save(data=response, file=fresp, log=log)

    table = BeautifulSoup(response, parser).find('table')
    tr_gen = (tr.find('td') for tr in table.find_all('tr'))
    proxies = [td.text for td in tr_gen if td]
    save(data='\n'.join(proxies), file=fpx, log=log)

    return proxies


def set_default(**kw):
    kw.setdefault('url', const.URL)
    kw.setdefault('fpx', const.FILE_PARSED_PROXIES)
    kw.setdefault('fresp', const.FILE_RESPONSE)
    kw.setdefault('parser', 'lxml')
    return kw
