#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

LOG_FILE_PROXIES = 'log/proxies'
LOG_FILE_RESPONSE = 'log/response'
URL = 'https://free-proxy-list.net/'


def save(data, file):
    with open(file, 'w') as f:
        f.write(data)


def parse_proxies(url=URL,
    file_proxies=LOG_FILE_PROXIES,
    file_response=LOG_FILE_RESPONSE,
) -> list:
    response = requests.get(url).text
    save(response, file_response)
    table = BeautifulSoup(response, 'lxml').find('table')
    px_gen = (tr.find('td') for tr in table.find_all('tr'))
    proxies = [td.text for td in px_gen if td]
    save('\n'.join(proxies), file_proxies)
    return proxies


if __name__ == '__main__':
    r = parse_proxies()
    print(f'{r=}')
