#!/usr/bin/env python
import sys

import requests
from bs4 import BeautifulSoup

from config.colors import color
from parsers.ctlnk.constants import url


def parse():
    ...


def save(data):
    ...


def main():
    data = parse()
    save(data)
    print('OK')


if __name__ == '__main__':
    main()
