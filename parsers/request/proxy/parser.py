#!/usr/bin/env python
"""The 'parser' module contains proxy parsers."""

__all__ = 'parse', 'parse_proxies'

import requests as _requests

if is_script := __name__ == '__main__':
    import sys as _sys; from os.path import dirname as _dn  # noqa: E401, E702
    # Append $PROJECT_DIR to use imports below
    _sys.path.append(_dn(_dn(__file__)))

from parsers.datatypes import HTML as _HTML
from parsers.exceptions import raise_notfound as _raise_notfound
from parsers.constants import Constant as _Constant
from parsers.rawdata_handlers import make_soup as _make_soup
from parsers.settings import Configuration as _Configuration
from parsers.storage.files import save_to_file as _save_to_file


def parse_proxies(cfg: _Configuration = _Configuration(), output=False):
    """Make request on `cfg`.url, parse response and return parsed proxies."""
    cfg = _setdefault_configs(cfg or _Configuration())
    source_page = _requests.get(cfg.url).text
    _save_to_file(data=source_page, file=cfg.file_response)
    proxies = _parse_table(source_page, cfg.parser)
    _save_to_file(data='\n'.join(proxies), file=cfg.file_parsed)
    return proxies


def _setdefault_configs(cfg: _Configuration) -> _Configuration:
    cfg.setdefaults(const=_Constant)
    return cfg


def _parse_table(page: _HTML, parser: str, tag='table'):
    """Return fetched IPs, ports from table > ResultSet[tr] > 1st,2nd td."""
    proxies = []
    soup = _make_soup(page, parser)
    table = soup.find(tag)
    try:
        rows = table.find_all('tr')  # pyright: ignore [reportOptionalMemberAccess]
    except AttributeError as AE:
        raise _raise_notfound(tag) from AE
    else:
        for td in rows:
            ip = td.select_one(_Constant.PARSE.SELECT_IP)
            port = td.select_one(_Constant.PARSE.SELECT_PORT)
            if ip and port:
                proxies.append(f'{ip.text}:{port.text}')
    return proxies


def parse(func=parse_proxies, configs: _Configuration = None, output=True) -> None:
    """Parse proxies with `func` and display parsed with pydoc.pager"""
    from pydoc import pager
    pager('\n'.join(func(configs, output=output)))


# $PROJECT_DIR/parsers/request/proxy/parser.py --parse
if is_script and _Constant.CLI.PARSE in _sys.argv:  # pyright: ignore [reportUnboundVariable]
    parse()
