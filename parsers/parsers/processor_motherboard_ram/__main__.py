#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import csv
import os
import random
import time
from contextlib import suppress
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def parse(url: str):
    page: str = load_page(url)
    category = url[:-1].rsplit('/', 1)[-1]
    parse_page(page, category)


def load_page(url: str, sleep: int = 0, ua: str = UserAgent().chrome) -> str:
    def timeout(status_code: int) -> int:
        return {
            503: random.uniform(2, 5),
            429: int(r.headers.get('Retry-After', random.uniform(100, 1000))),
        }[status_code]

    time.sleep(sleep)
    print(f'GET: {url}')
    r = requests.get(url, headers={'user-agent': ua})
    print('Status code: ', r.status_code)
    if r.status_code == 429:
        print(f'Too many redirect! Retry-After: {r.headers.get("Retry-After")}')
    time.sleep(random.uniform(2., 4.))
    return r.text if r.ok else load_page(url, timeout(r.status_code))


def beautifulsoup_parser(func, parser: str = 'lxml'):
    def wrapper(page, *args, **kwargs):
        soup = BeautifulSoup(page, parser)
        return func(soup, *args, **kwargs)
    return wrapper


@beautifulsoup_parser
def parse_page(page: str, category: str):
    for a in page.find_all('a', {'class': 'ProductCardHorizontal__title'}):
        print('---', a.text.strip(), sep='\n')
        url_item_propertis = f'{URL_BASE}{a.get("href")}/properties'
        time.sleep(random.uniform(7., 13.))
        page = load_page(url_item_propertis)
        data = parse_item(page)
        save(data, category)


@beautifulsoup_parser
def parse_item(page: str) -> list:
    item = page.h1.text.strip().replace('Характеристики ', '')
    data, data_names, data_values = [], ['Наименование'], [item]

    for div in page.find_all('div', {'class': 'SpecificationsFull'}):
        with suppress(AttributeError):
            print(f'{div.h4.text.strip()}:')
        spec = div.find('div', {'class': 'Specifications'})
        with suppress(AttributeError):
            for row in spec.find_all('div', {'class': 'Specifications__row'}):
                with suppress(AttributeError):
                    row.div.div.decompose()
                spec_name = row.find('div', class_='Specifications__column_name').text.strip()
                spec_value = row.find('div', class_='Specifications__column_value').text.strip()
                print(f' - {spec_name}: {spec_value}')
                data_names.append(spec_name)
                data_values.append(spec_value)  
                time.sleep(random.ranuniformdint(1., 3.))
    data.append(data_names)
    data.append(data_values)
    return data


def save(data: list, category: str):
    file = f'data/{category}.csv'
    print(f'Data saving to {file=}...')
    with open(file, 'a') as f:
        writer = csv.writer(f)
        is_empty: bool = os.stat(file).st_size == 0
        writer.writerows(data if is_empty else data[1:])
    print('Saved successfull!\n')


if __name__ == '__main__':
    print('\nProgram starting ...')

    URL_BASE = 'https://www.citilink.ru'
    urls = [
        f'{URL_BASE}/catalog/materinskie-platy/',
        f'{URL_BASE}/catalog/processory/',
        f'{URL_BASE}/catalog/moduli-pamyati/',
    ]

    with Pool(len(urls)) as pool:
        pool.map(parse, urls)

    print('\nProgram finished!')
