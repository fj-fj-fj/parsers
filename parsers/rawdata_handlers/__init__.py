from bs4 import BeautifulSoup
from requests.exceptions import JSONDecodeError


def make_soup(html: str, parser: str) -> BeautifulSoup:
    return BeautifulSoup(html, parser)
