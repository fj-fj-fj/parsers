import logging
import sqlite3
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
        self.connection = sqlite3.connect(config.database_name)
        self.cursor = self.connection.cursor()

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
            'name_ticker', 'price', 'day', 'week', 'market_cap', 'volume', 'circulating_supply'
        ])
        # replace: bincoin1BTC -> bincoinBTC
        df['name_ticker'].replace(['\d', ' '], '', regex=True, inplace=True)
        return df

    def save_to_sql(self, df: pd.DataFrame) -> None:
        database_name = config.database_name.split('.')[0]
        try:
            with self.connection as conn:
                logger.info('Successfully connected to SQLite')
                df.to_sql(database_name, conn)
        except sqlite3.Error as error:
            logger.error('Error with connection to sqlite', error)
        finally:
            if self.connection:
                self.connection.close()
            logger.info('The SQLite connection is closed')

    def run(self) -> None:
        url = 'https://coinmarketcap.com/'
        html: str = self.load_page(url)
        two_dimensional_list = self.parse_page(html)
        df = self.get_dataframe(two_dimensional_list)
        
        logger.debug(f'DataFrame:\n{df}')
        self.save_to_sql(df)


if __name__ == '__main__':
    parser = Client()
    parser.run()

    logger.debug('\nTest sql select')
    conn = sqlite3.connect(config.database_name)
    sql_query = f"select * from {config.database_name.split('.')[0]} limit 4"
    logger.debug(pd.read_sql(sql_query, conn))
    conn.commit()
    conn.close()
    