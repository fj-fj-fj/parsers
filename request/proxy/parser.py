"""Proxy parsing module"""

__all__ = 'parse', 'parse_proxies'

import requests
from bs4 import BeautifulSoup

from request.constants import CONSTANTS as const
from utils import save_to_file


def parse(**kw):
    """Parse proxies with and return parsed"""
    response = parse_proxies(log=True, **kw)
    return f'{response=}'


def parse_proxies(log=False, **kw) -> list[str]:
    """Parse proxies from <url>"""
    url, fpx, fresp, parser = set_defaults(**kw).values()
    html = get(url).text
    save_to_file(data=html, file=fresp, log=log)

    proxies = []
    table = BeautifulSoup(html, parser).find('table')
    for tr in table.find_all('tr'):
        ip = tr.select_one(const.SPIDER.SELECT_IP)
        port = tr.select_one(const.SPIDER.SELECT_PORT)
        if ip and port:
            proxies.append(f'{ip.text}:{port.text}')

    save_to_file(data='\n'.join(proxies), file=fpx, log=log)
    return proxies


def set_defaults(**kw):
    kw.setdefault('url', const.URL.FPL_PROXY_URL)
    kw.setdefault('fpx', const.FILE.PARSED_PROXIES)
    kw.setdefault('fresp', const.FILE.RESPONSE_PROXY)
    kw.setdefault('parser', 'lxml')
    return kw


def get(url: str) -> requests.Response:
    return requests.get(url)
