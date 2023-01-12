#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# mypy: ignore-errors
"""
Получить с русской вики список всех животных (Категория:Животные по алфавиту)
и вывести количество животных на каждую букву алфавита.
Результат должен получиться в следующем виде:
А: 642, Б: 412, ...

"""
import logging
import os
import os.path
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from random import uniform
from time import sleep
from typing import NoReturn, TypeVar

import bs4
import requests
from fake_useragent import UserAgent as ua

ANIMALS_LIST = 'animals_list'
ANIMALS_COUNT = 'animals_count'
ROOT_PARSER_DIR = f'parsers/wiki'
PARSERS_WIKI_DATA = f'{ROOT_PARSER_DIR}/data'

T = TypeVar('T', bound='Client')


class Client:

    def __init__(
        self: T,
        url: str,
        tmpfile: str,
        headers: str = ua().chrome,
        timeout: int = 6,
        read_logs: bool = False,
    ):
        self._session = requests.Session()
        self._session.headers = headers
        self._session.timeout = timeout
        self._start = datetime.now()

        self._result_count: dict[str, int] = self._generate_animals_dict(int)
        self._result_list: dict[str, list[str]] = self._generate_animals_dict(list)

        self._url = url
        self._read_logs = read_logs

        self._set_logger(tmpfile)


    @staticmethod
    def _generate_animals_dict(func) -> dict[str, int] | dict[str, list[str]]:
        """Generate `dict` with default `int` or `list`."""
        class DefaultDict(defaultdict):
            __repr__ = dict.__repr__

        letter_default = DefaultDict(func)

        for litera in map(chr, [*range(1040, 1072), *range(65, 91)]):
            letter_default[litera]

        return letter_default


    @staticmethod
    def _save(
        data: dict,
        file: str,
        dir: str = PARSERS_WIKI_DATA,
        mode: str = 'w'
    ):
        os.makedirs(dir, exist_ok=True)

        with open(os.path.join(dir, file), mode) as f:
            f.write(str(data))


    @staticmethod
    def _stop_program(
        result_count: dict[str, int] | dict[str, list[str]],
        start_program: datetime,
        traceback_info_levels: int = 0
    ) -> NoReturn:
        sys.tracebacklimit = traceback_info_levels
        sys.exit(
            f'Result count: {result_count}\n'
            f'Time: {datetime.now() - start_program}'
        )


    def _set_logger(
        self: T,
        tmpfile: str,
        name: str = __name__,
        level: int = logging.DEBUG,
        formatter: str = "%(message)s",
        mode: str = 'w',
    ):
        def file_handler() -> logging.FileHandler:
            fh = logging.FileHandler(tmpfile, mode=mode)
            fh.setLevel(level)
            fh.setFormatter(logging.Formatter(formatter))
            return fh

        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.addHandler(file_handler())


    def run(self: T):
        self._load_page()._cook_soup()._parse_page()


    def _load_page(self: T) -> T:
        self._html: str = self._session.get(url=self._url).text
        return self


    def _cook_soup(self: T, parser: str = 'lxml') -> T:
        self._soup: bs4.element.Tag = bs4.BeautifulSoup(self._html, parser)
        return self


    def _parse_page(self: T):
        categories = self._soup.body.find_all('div', class_='mw-category-group')

        for c in categories:
            self._result_list[c.h3.text] += [li.text for li in self._find_li(c)]
            self._result_count[c.h3.text] += len(self._find_li(c))
            self._logger.warning(f'Считаем зверей ...\n{self._result_count}')

        self._check_next_page()


    def _check_next_page(self: T, iteration_sleep: tuple[int, int] = (1, 9)):
        navbox = self._soup.body.find(id='mw-pages')

        for a in navbox.h2.find_next_siblings('a'):
            if a.text == (next_page := 'Следующая страница'):
                self._logger.debug(next_page + ':')
                sleep(uniform(*iteration_sleep))
                self._click_next_page(a)
        else:
            self._save(self._result_list, file=ANIMALS_LIST)
            self._save(self._result_count, file=ANIMALS_COUNT)
            self._read_logs and os.system('pkill -9 -x tail')
            self._stop_program(
                result_count=self._result_count,
                start_program=self._start,
            )


    def _click_next_page(self: T, link: bs4.element.Tag):
        base_url, *_ = self._url.rsplit('/', 2)
        self._url = f'{base_url}/{link["href"]}'
        self._logger.debug(f'click {self._url}')

        self._load_page()._cook_soup()._parse_page()


    def _find_li(self: T, group: bs4.element.Tag) -> list[str]:
        return [li for li in group.find('ul').find_all('li')]


URL = r'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'


with tempfile.NamedTemporaryFile(dir=ROOT_PARSER_DIR, delete=True) as tmpfile:
    temp_file_name = tmpfile.name
    with open(os.path.join(ROOT_PARSER_DIR, 'tail_f_logs.sh'), 'w') as script:
        script.write(f'#/usr/bin/sh\ntail -f {temp_file_name}\n')

    parser = Client(url=URL, tmpfile=temp_file_name, read_logs=True)
    parser.run()
