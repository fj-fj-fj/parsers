#!/usr/bin/env python
"""Module 'parser' that contains proxy parsers."""

__all__ = 'parse', 'parse_proxies'

import requests

if is_script := __name__ == '__main__':
    import sys; from os.path import dirname  # noqa: E401, E702
    # Append $PROJECT_DIR to use imports below
    sys.path.append(dirname(dirname(__file__)))

from datatypes import HTML
from datatypes import ProxyList
from exceptions import raise_notfound
from constants import ConstantStorage
from parsers.utils import make_soup
from settings import Configuration
from storage.files import save_to_file


def parse_proxies(cfg: Configuration = Configuration(), output=False) -> ProxyList:
    """Make request on cfg.url, parse response, return parsed proxies."""
    cfg = _setdefault_configs(cfg or Configuration())
    source_page = requests.get(cfg.url).text
    save_to_file(data=source_page, file=cfg.file_response, log=output)
    proxies = _parse_table(source_page, cfg.parser)
    save_to_file(data='\n'.join(proxies), file=cfg.file_parsed, log=output)
    return proxies


def _setdefault_configs(cfg: Configuration) -> Configuration:
    cfg.setdefaults(const=ConstantStorage)
    return cfg


def _parse_table(page: HTML, parser: str, tag='table') -> ProxyList:
    """Return fetched IPs, ports from table > ResultSet[tr] > 1st,2nd td."""
    proxies = []
    soup = make_soup(page, parser)
    table = soup.find(tag)
    try:
        rows = table.find_all('tr')  # pyright: ignore [reportOptionalMemberAccess]
    except AttributeError as AE:
        raise raise_notfound(tag) from AE
    else:
        for td in rows:
            ip = td.select_one(ConstantStorage.PARSE.SELECT_IP)
            port = td.select_one(ConstantStorage.PARSE.SELECT_PORT)
            if ip and port:
                proxies.append(f'{ip.text}:{port.text}')
    return proxies


def parse(func=parse_proxies, configs: Configuration = None, output=True) -> None:
    """Parse proxies with `func` and display parsed with pydoc.pager"""
    from pydoc import pager
    pager('\n'.join(func(configs, output=output)))


# $PROJECT_DIR/src/request/proxy/parser.py --parse
if is_script and ConstantStorage.CLI.PARSE in sys.argv:
    parse()
