from bs4 import BeautifulSoup


def make_soup(html: str, parser: str) -> BeautifulSoup:
    return BeautifulSoup(html, parser)
