from bs4 import BeautifulSoup
from requests.exceptions import JSONDecodeError


def make_soup(html: str, parser: str) -> BeautifulSoup:
    return BeautifulSoup(html, parser)


def convert_response_to_str_or_json(response) -> str | list:
    try:
        return response.json()
    except JSONDecodeError:
        return response.text
