# 1. Получить html coinmarketcap.com
# 2. Спарсить имя, тикер, цену и урл монеты
# 3. Сохранить в БД используя ОРМ алхимию
# 4. Протестировать, сделав полную выборку
import logging

import requests
from bs4 import BeautifulSoup

from config import COINMARKETCAP_URL
from models import CoinsTable, session


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('parser2')


def get_html(url: str) -> str:
    response = requests.get(url, timeout=5)
    logger.debug(f'Response: {response.status_code}')
    return response.text


def parse_page(html: str) -> list:
    data = [] # List[Tuple(str, str, float, str), ...]
    table = BeautifulSoup(html, 'lxml').table

    for tr in table.tbody.find_all('tr'):
        tds = tr.find_all('td')
        try:
            name = tds[2].a.p.text
            ticker = tds[2].a.div.div.div.p.text
            price = float(tds[3].a.text[1:].replace(',', ''))
        except AttributeError:
            name = tds[2].find_next('span').find_next('span').text
            ticker = tds[2].find_next('span')\
                     .find_next('span').find_next('span').text
            price = float(tds[3].text[1:].replace(',', ''))
        except IndexError:
            continue # pass ad

        source = COINMARKETCAP_URL + tds[2].a.get('href')
        data.append((name, ticker, price, source))

    return data


def save_to_sql(data: list) -> None:
    for name_ticker_price_source in data:
        instance = CoinsTable(*name_ticker_price_source)
        session.add(instance)
    session.commit()


def main() -> None:
    html: str = get_html(COINMARKETCAP_URL)
    data: list = parse_page(html)
    save_to_sql(data)


if __name__ == '__main__':
    main()

    # test with query
    from test_parser2 import Test

    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    logger.info(f'\a\vTest `SELECT * FROM coinmarketcap ORDER BY`\n')

    Test.TABLE = CoinsTable
    Test.SESSION = session
    select_coins = Test()
    select_coins.all()
