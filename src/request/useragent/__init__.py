"""Package 'useragent' that contains useragent tools."""

__all__ = 'gen_useragents_cycle',

from itertools import cycle
from typing import Iterator


def gen_useragents_cycle(file: str = None) -> Iterator[str]:
    """Return itertools.cycle(useragents `file` or 'Chrome 106.0 Win10')."""
    if file is None:
        return cycle([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, например Gecko) "
            "Chrome/106.0.0.0 Safari/537.36"])

    with open(file) as useragents:
        return cycle(useragents.readlines())
