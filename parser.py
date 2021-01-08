# 
import logging
from typing import List

import bs4
import requests
import pandas as pd

import config


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('parser')

class Client:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {**config.headers}

    def load_page(self, url: str) -> str:
        r: requests.models.Response = self.session.get(url, timeout=5)
        logger.debug(f'Status code: {r.status_code}')
        return r.text

    def parse_page(self, html: str) -> List[List[str]]:
        list_of_lists = []
        soup = bs4.BeautifulSoup(html, 'lxml')
        table: bs4.element.Tag = soup.find('table')

        for tr in table.tbody.find_all('tr'):
            list_of_lists.append([td.get_text() for td in tr.find_all('td') if td.text])

        for sublist in range(10):
            list_of_lists[sublist].pop(0)

        del list_of_lists[10] # ad
        return list_of_lists

    def get_dataframe(self, two_dimensional_list: List[List[str]]) -> pd.DataFrame:
        df = pd.DataFrame(two_dimensional_list, columns=[
            'Name_TICKER', 'Price', '24h', '7d', 'Market_cap', 'Volume', 'Circulating_supply'
        ])
        # replace: bincoin1BTC -> bincoinBTC
        df['Name_TICKER'].replace(['\d', ' '], '', regex=True, inplace=True)
        return df

    def save_result(self):
        pass

    def run(self):
        url = 'https://coinmarketcap.com/'
        html: str = self.load_page(url)
        two_dimensional_list = self.parse_page(html)
        df = self.get_dataframe(two_dimensional_list)
        print(df[:30])
        logger.debug('Done!')

        self.save_result()


if __name__ == '__main__':
    parser = Client()
    parser.run()
    