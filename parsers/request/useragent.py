"""The 'useragent' module contains useragent tools."""

__all__ = 'gen_useragents_cycle',

from itertools import cycle as _cycle
from typing import Iterator as _Iterator


def gen_useragents_cycle(file: str = None) -> _Iterator[str]:
    """Return itertools.cycle(`file` or 'Chrome 106.0 Win10')."""
    if file is None:
        return _cycle([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, например Gecko) "
            "Chrome/106.0.0.0 Safari/537.36"])
    with open(file) as useragents:
        return _cycle(useragents.readlines())
