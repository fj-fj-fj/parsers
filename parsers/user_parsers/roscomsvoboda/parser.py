#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

if is_script := __name__ == '__main__':
    import sys; from os.path import dirname  # noqa: E401, E702
    # Append $PROJECT_DIR to use imports below
    # sys.path.append(dirname(dirname(__file__)))
    pass

from parsers.rawdata_handlers import convert_response_to_str_or_json
from parsers.storage.files import context_storage

from .constants import URL, PARSED_DIR


def parse(URL):
    response = requests.get(URL)
    converted = convert_response_to_str_or_json(response)

    file = PARSED_DIR
    context_storage(converted, file).save(converted)


def main():
    parse(URL)


if __name__ == '__main__':
    main()
