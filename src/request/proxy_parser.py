#!/usr/bin/env python
"""Module 'parser' that contains proxy parsers."""

__all__ = 'parse', 'parse_proxies'

if is_script := __name__ == '__main__':
    import sys; from os.path import dirname  # noqa: E401, E702
    # Append $PROJECT_DIR to use imports below
    sys.path.append(dirname(dirname(dirname((__file__)))))
    from config.REPL.helpers import set_interactive_mode
    set_interactive_mode()

from config import Configuration
from exceptions import raise_notfound
from request._types import ProxyList
from request.constants import ConstantStorage as const
from utils import get
from utils import make_soup
from utils import save_to_file


def parse_proxies(cfg: Configuration = Configuration(), output=False) -> ProxyList:
    """Return parsed proxies."""
    cfg = _set_default_values(cfg or Configuration())
    source_page = get(cfg.url).text
    save_to_file(data=source_page, file=cfg.file_response, log=output)

    proxies = _parse_table(source_page, cfg.parser)
    save_to_file(data='\n'.join(proxies), file=cfg.file_parsed, log=output)

    return proxies


def _parse_table(page: str, parser: str, tag='table') -> ProxyList:
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
            ip = td.select_one(const.PARSE.SELECT_IP)
            port = td.select_one(const.PARSE.SELECT_PORT)
            if ip and port:
                proxies.append(f'{ip.text}:{port.text}')
    return proxies


def _set_default_values(cfg: Configuration) -> Configuration:
    cfg.setdefault(cfg.key.url, const.URL.FPL_PROXY_URL)
    cfg.setdefault(cfg.key.file_parsed, const.FILE.PARSED_PROXIES)
    cfg.setdefault(cfg.key.file_response, const.FILE.PROXY_RESPONSE)
    cfg.setdefault(cfg.key.parser, const.PARSE.PARSER)
    return cfg


def parse(func=parse_proxies, configs: Configuration = None, output=True) -> None:
    """Parse proxies with `func` and display parsed with pydoc.pager"""
    from pydoc import pager
    pager('\n'.join(func(configs, output=output)))


# $PROJECT_DIR/src/request/proxy/parser.py --parse
if is_script and const.CLI.PARSE in sys.argv:
    parse()
