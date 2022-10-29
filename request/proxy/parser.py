#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

try:
    from request.proxy.constants import const
    from utils import save
except ModuleNotFoundError:
    __import__('patch').update_syspath(__file__)
    from request.proxy.constants import const
    from utils import save

__all__ = 'parse', 'parse_proxies'


def parse(**kw):
    """Parse proxies with print parsed"""
    response = parse_proxies(**kw)
    print(f'{response=}')


def parse_proxies(**kw) -> list:
    """Parse proxies from `constants.const.URL`"""
    url, fpx, fresp, parser = set_default(**kw).values()

    response = requests.get(url).text
    save(data=response, file=fresp)

    table = BeautifulSoup(response, parser).find('table')
    tr_gen = (tr.find('td') for tr in table.find_all('tr'))
    proxies = [td.text for td in tr_gen if td]
    save(data='\n'.join(proxies), file=fpx)

    return proxies


def set_default(**kw):
    kw.setdefault('url', const.URL)
    kw.setdefault('fpx', const.FILE_PARSED_PROXIES)
    kw.setdefault('fresp', const.FILE_RESPONSE)
    kw.setdefault('parser', 'lxml')
    return kw
