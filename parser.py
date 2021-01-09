# Получить HTML главной страницы coinmarketcap
# Вытащить из таблицы все данные по монетам из первой сотни
# Очистить данные и сгрузить в DataFrame
# Сохранить в базу данных
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
    """Parse the Coinmarketcap first page"""
    def __init__(self):
        """Initialize session, DB connection, cursor and add HTTP-headers"""
        self.session: requests.sessions.Session = requests.session()
        self.session.headers: dict = {**config.headers}
        self.connection: sqlite3.Connection = sqlite3.connect(config.database_name)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def load_page(self, url: str) -> str:
        """Get HTML Coinmarketcap first page"""
        r: requests.models.Response = self.session.get(url, timeout=5)
        logger.debug(f'Status code: {r.status_code}')
        return r.text

    def parse_page(self, html: str) -> List[List[str]]:
        """Parse HTML.
           
           Get the name and ticker, price, volume and
           other info about the first hundred coins.
        """
        list_of_lists = []
        soup = bs4.BeautifulSoup(html, 'lxml')
        table: bs4.element.Tag = soup.find('table')

        for tr in table.tbody.find_all('tr'):
            list_of_lists.append([td.get_text() for td in tr.find_all('td') if td.text])
        
        # ОЧИСТИТЬ ДАННЫЕ: удалить лишний столбец первой 10ки монет:
        for sublist in range(10):
            list_of_lists[sublist].pop(0)

        del list_of_lists[10] # ad
        return list_of_lists

    def get_dataframe(self, two_dimensional_list: List[List[str]]) -> pd.DataFrame:
        """Get DataFrame from 2D array"""
        df = pd.DataFrame(two_dimensional_list, columns=[
            'name_ticker', 'price', 'day', 'week', 'market_cap', 'volume', 'circulating_supply'
        ])
        # replace: bincoin1BTC -> bincoinBTC
        df['name_ticker'].replace(['\d', ' '], '', regex=True, inplace=True)
        return df

    def save_to_sql(self, df: pd.DataFrame) -> None:
        """Dump DataFrame to the (coinmarketcap table) coinmarketcap.db"""
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
    