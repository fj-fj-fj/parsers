#!/usr/bin/env python
import json
import logging
from multiprocessing import Pool
from pathlib import Path
from random import uniform
from time import sleep
from typing import Any, Optional

import requests
# isort: off
from requests.structures import CaseInsensitiveDict

from base_config import CONFIGURATION as CONF
# isort: on


class Client:

    def __init__(
        self,
        url: str = CONF.URL,
        headers: CaseInsensitiveDict[str] = CONF.HEADERS,
        params: dict[str, int] = CONF.PARAMS,
    ) -> None:
        self._logger = logging.getLogger(__name__)
        self._session = requests.Session()
        self._session.headers = headers
        self._requests_params = params
        self._url = url
        self._data: dict[str, Any] = {}

        Client.makedir(CONF.DIR)

    @staticmethod
    def _write_json(data: dict, prefix: str, mode: str = 'w') -> None:
        with open(CONF.FILES.JSON.format(prefix), mode) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def _write_IDs_to_txt(post_id: str, mode: str = 'a') -> None:
        with open(CONF.FILES.TXT, mode) as file:
            file.write(post_id + '\n')

    @staticmethod
    def _read_IDs_from_txt(mode: str = 'r') -> list[str]:
        with open(CONF.FILES.TXT, mode) as file:
            return file.readlines()

    @staticmethod
    def makedir(name: str) -> None:
        Path(name).mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        self._logger.debug(f'Parsing "{CONF.URL}" ...')
        self._load_page()
        self._parse()

    def _parse(self) -> None:
        total_articles = self._data['paginator']['total']
        pagination = total_articles // 100 + 1

        for page in range(pagination):
            self._parse_page()
            if pagination - page == 1:
                self._requests_params['perPage'] = total_articles % 100
            self._requests_params['page'] += 1

        self._url = self._url.replace('region?', 'item/')

        with Pool(30) as p:
            p.map(self._save_all_articles, Client._read_IDs_from_txt())

    def _save_all_articles(self, post_id: str) -> None:
        post_id = post_id.strip()
        self._load_page(item_id=post_id)
        parsed_data = self._data
        Client._write_json(data=parsed_data, prefix=post_id)
        self._logger.debug(f'Article with ID:{post_id} saved.')

    def _parse_page(self) -> None:
        self._load_page(params=self._requests_params)
        self._fetch_ids_from_json()

    def _load_page(
        self,
        item_id: str = '',
        params: Optional[dict[str, int]] = None
    ) -> None:
        sleep(uniform(1, 3))
        url = ''.join((self._url, item_id))
        self._data = self._session.get(url=url, params=params).json()

    def _fetch_ids_from_json(self) -> None:
        self._logger.debug('Article IDs saving ...')
        for post in self._data.get('data'):  # type: ignore
            Client._write_IDs_to_txt(str(post['id']))


if __name__ == '__main__':
    (scraper := Client()).run()
    scraper._logger.debug('Done!')
