import csv
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from contextlib import suppress
from fake_useragent import UserAgent

URL_BASE = 'https://www.citilink.ru'


def parse(url: str, category: str):
    page: str = load_page(url)
    parse_page(page, category)


def load_page(url: str, sleep: int = 0, ua: str = UserAgent().chrome) -> str:
    def timeout(status_code: int) -> int:
        return {503: 3, 429: random.uniform(200, 500)}[status_code]

    time.sleep(sleep)
    print(f'GET: {url}')
    r = requests.get(url, headers={'user-agent': ua})
    print('Status code: ', r.status_code)
    time.sleep(random.uniform(2., 4.))
    return r.text if r.ok else load_page(url, timeout(r.status_code))


def beautiful_soup(func, parser: str = 'lxml'):
    def wrapper(page, *args, **kwargs):
        soup = BeautifulSoup(page, parser)
        return func(soup, *args, **kwargs)
    return wrapper


@beautiful_soup
def parse_page(page: str, category: str) -> list:
    for a in page.find_all('a', {'class': 'ProductCardHorizontal__title'}):
        print('---', a.text.strip(), sep='\n')
        url_item_propertis = f'{URL_BASE}{a.get("href")}/properties'
        page = load_page(url_item_propertis)
        data = parse_item(page)
        save(data, category)


@beautiful_soup
def parse_item(page: str) -> list:
    item = page.h1.text.strip().replace('Характеристики ', '')
    data, data_names, data_values = [], ['Наименование'], [item]
    # print(item, '-' * len(item), sep='\n')

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
    time.sleep(random.uniform(2., 4.))
    return data


def save(data: list, category: str):
    file = f'data/{category}.csv'
    print(f'Data saving to {file=}...')
    with open(file, 'a') as f:
        writer = csv.writer(f)
        is_empty = os.stat(file).st_size == 0
        writer.writerows(data if is_empty else data[1:])
    print('Saved successfull!\n')


if __name__ == '__main__':
    for category in ('materinskie-platy', 'processory', 'moduli-pamyati'):
        url = f'{URL_BASE}/catalog/{category}/'
        print('\nProgram starting ...')
        print(f'Parse category: {category}\n')
        parse(url, category)
        print('\nProgram finished!')
