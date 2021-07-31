#!/usr/bin/env python
import sys
from random import random
from time import sleep
from typing import Optional, Set

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from fake_useragent import UserAgent

BASE_LINK = 'https://www.profdisplays.ru/catalog/touch-displays/'
FILE = 'discontinued_tech/parsed_data.txt'

HEADERS: dict = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-lanquage': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'connection': 'keep-alive',
    'user-agent': UserAgent().random,
    'x-requested-with': 'XMLHttpRequest',
}

DISCONTINUED_PRODUCTS: Set[str] = set()

_html_or_error = str
_error_or_none = Optional[str]


def _load_page(number, url = BASE_LINK, timeout = 10) -> _html_or_error:
    print(f'Making a get request with {number=} ...')
    return ('Connection Error',
        (response := requests.get(url,
            params=dict(PAGEN=1, PAGEN_2=number, PAGEN_1=number),
            headers=HEADERS,
            timeout=timeout,
        )).text
    )[response.status_code == requests.codes.ok]


def _parse_page(soup: BeautifulSoup):
    print(f'Parse ...')
    items: ResultSet = soup.select('div.item__image-field')
    for item in items:
        if item.span and item.span.text == 'Снят с производства':
            product_name = item.a.img['alt'] + '\n'
            DISCONTINUED_PRODUCTS.add(product_name)


def _check_page_number(soup: BeautifulSoup) -> int:
    next_page = soup.select_one('a.is-active').next_sibling.next_sibling
    return int(next_page.text) if next_page is not None else 0


def parse(page_number = 1) -> _error_or_none:
    sleep(random() + page_number)
    response: str = _load_page(page_number)
    if 'Error' in response: return response

    html = response
    soup = BeautifulSoup(html, 'lxml')
    _parse_page(soup)

    if (number := _check_page_number(soup)):
        parse(number)


def save_data(file = FILE, parsed_data: set = DISCONTINUED_PRODUCTS):
    print(f'Saving into {FILE} ...')
    with open(file, 'w') as f:
        f.writelines(parsed_data)


def main():
    error = parse()

    DISCONTINUED_PRODUCTS and save_data()
    print('Done' if not error else error)


if __name__ == '__main__':
    if sys.argv == '--save':
        with open('discontinued_tech/html.html', 'w') as f:
            f.write(requests.get(BASE_LINK).text)
    else:
        main()
