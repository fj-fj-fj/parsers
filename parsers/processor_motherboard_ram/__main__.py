import csv
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from contextlib import suppress
from fake_useragent import UserAgent


def parse(url: str):
    print('Program starting ...\n')
    # page = load_page(url)
    with open('data/page.html') as page:
        data = parse_page(page)
    save(data)
    print('\nProgram finished!')


def load_page(url: str, ua: str = UserAgent().chrome) -> str:
    r = requests.get(url, headers={'user-agent': ua})
    print(f'{url=}')
    print('Status code: ', r.status_code)
    time.sleep(2)
    return r.text


def parse_page(page: str) -> list:
    soup = BeautifulSoup(page, 'lxml')
    item = soup.h1.text.strip().replace('Характеристики ', '')
    data, data_names, data_values = [], ['Наименование'], [item]
    print(item, '-' * len(item), sep='\n')

    for div in soup.find_all('div', {'class': 'SpecificationsFull'}):
        with suppress(AttributeError):
            print(f'{div.h4.text.strip()}:')
        spec = div.find('div', {'class': 'Specifications'})
        with suppress(AttributeError):
            for row in spec.find_all('div', {'class': 'Specifications__row'}):
                with suppress(AttributeError):
                    row.div.div.decompose()
                spec_name = row.find('div', class_='Specifications__column_name').text.strip()
                spec_value = row.find('div', class_='Specifications__column_value').text.strip()
                print(f'  {spec_name}: {spec_value}')
                data_names.append(spec_name)
                data_values.append(spec_value)  
                # time.sleep(random.ranuniformdint(1., 3.))
    data.append(data_names)
    data.append(data_values)
        # time.sleep(random.uniform(2., 4.))
    return data


def save(data, file='data/foo.scv'):
    print(f'\nData saving to {file=}...')
    with open(file, 'a') as f:
        writer = csv.writer(f)
        is_empty = os.stat(file).st_size == 0
        writer.writerows(data if is_empty else data[1:])
    print('Saved successfull!')


if __name__ == '__main__':
    url = 'https://www.citilink.ru/product/materinskaya-plata-asrock-a320m-dvs-r4-0-socketam4-amd-a320-matx-ret-1120710/properties/'
    parse(url)
