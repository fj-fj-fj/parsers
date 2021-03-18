import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String

import config


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.pool")
logger = logging.getLogger('parser2')

# dialect+driver://username:password@host:port/database
DB_URL = '{}+{}://{}:{}@{}:{}/{}'.format(*config.POSTGRES.values())
test = 'sqlite:///:memory:'

engine = create_engine(test)
# engine = create_engine(DB_URL)

session = sessionmaker(bind=engine)()

Base = declarative_base()


class CoinsTable(Base):
    __tablename__ = 'coinmarketcap'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ticker = Column(String)
    price = Column(Float)
    source = Column(String)

    def __init__(self, name, ticker, price, source):
        self.name = name
        self.ticker = ticker
        self.price = price
        self.source = source

    def __repr__(self):
        return '<CoinsTable({}, {}, {}, {})>'.format(*self.__dict__.values())


Base.metadata.create_all(engine)

if __name__ == '__main__':
    logger.debug(f'SQLAlchemy version: {sqlalchemy.__version__}')
