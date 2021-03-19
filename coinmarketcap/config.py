try:
    from misc import uname, passwd
except (ModuleNotFoundError, ImportError) as e:
    print(repr(e),
         '\nSet password and uname to coinmarketcap/config/POSTGRES config')

COINMARKETCAP_URL = 'http://coinmarketcap.com'

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/84.0.4147.135 Safari/537.36',
            'Accept-Lanquage': 'ru',
}

# sqlite3
database_name = 'coinmarketcap.db'

# https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
POSTGRES = {
    'dialect': 'postgresql',
    'driver': 'psycopg2',
    'username': uname,
    'password': passwd,
    'host': "localhost",
    'port': 5432,
    'database': "coinmarketcap"
}
