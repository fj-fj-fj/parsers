#!/usr/bin/env python
"""This module contains parsing proxy tools."""

__all__ = 'parse', 'parse_proxies'

if script := __name__ == '__main__':
    import os, sys; from os.path import dirname  # noqa: E401, E702
    # Append root project to use imports below
    sys.path.append(dirname(dirname(dirname((__file__)))))
    # Use interactove mode
    os.environ['PYTHONINSPECT'] = '-i'

from exceptions import raise_notfound
from request.constants import CONSTANTS as const
from utils import get
from utils import make_soup
from utils import save_to_file


def parse_proxies(out=False, **kw) -> list[str]:
    """Return parsed proxies (get request kw[url])."""
    url, fparsed, fhtml, parser = set_default_values(**kw).values()
    proxies = []

    html = get(url).text
    save_to_file(data=html, file=fhtml, log=out)

    # Fetch IPs, ports from table > ResultSet[tr] > 1st,2nd td
    table = make_soup(html, parser).find('table')
    try:
        rows = table.find_all('tr')  # pyright: ignore [reportOptionalMemberAccess] # noqa E501
    except AttributeError as AE:
        raise raise_notfound('Tag') from AE
    else:
        for td in rows:
            ip = td.select_one(const.SPIDER.SELECT_IP)
            port = td.select_one(const.SPIDER.SELECT_PORT)
            if ip and port:
                proxies.append(f'{ip.text}:{port.text}')

    save_to_file(data='\n'.join(proxies), file=fparsed, log=out)
    return proxies


def parse(func=parse_proxies, out=True, **configns):
    """Parse proxies with `func` and print parsed unsing pydoc.pager"""
    from pydoc import pager
    pager(func(out=out, **configns))


def set_default_values(**kw):
    kw.setdefault('url', const.URL.FPL_PROXY_URL)
    kw.setdefault('fparsed', const.FILE.PARSED_PROXIES)
    kw.setdefault('fresponce', const.FILE.RESPONSE_PROXY)
    kw.setdefault('parser', const.SPIDER.PARSER)
    return kw


if script and const.CLI.PARSE in sys.argv:
    parse()
