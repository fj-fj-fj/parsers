#!/usr/bin/env python
"""# TODO: clean up \U0001F4A9 and write docsting"""

import requests as _requests

if is_script := __name__ == '__main__':
    __package__ = 'parsers.user_parsers.test_template'

    def fix_path():
        '''Fix sys.path and die.'''
        from sys import path
        path.insert(0, path[0] + 3 * '/..')
        global fix_path; del fix_path  # noqa: E702
    fix_path()

# 'Parsers' imports
from ...constants import Constant as _Constant
from ...handlers import Handler as _Handler
from ...handlers import handle_data as _handle_data
from ...handlers import HandledResponse as _HandledResponse
from ...imports import snoop as _snoop

# 'test_template' template local imports
from .constants import URL
from .constants import PARSED_DIR

URL = URL or input(_Constant.PROMPT.ENTER_URL_OR_FALSE)


# @_snoop
def _load_page(url: str, **request_kwargs) -> _Handler:
    """Make request and return received data `Handler`"""
    response = _requests.get(url, **request_kwargs)
    return _handle_data(response, PARSED_DIR)


# @_snoop
def _parse(data: _HandledResponse):
    """Extract data"""
    result = None
    if data.is_json:
        result = ...
    else:
        soup = data.make_soup()
        print(11, soup)
        result = ...
    return result


# @_snoop
def _save_result(data) -> None:
    """# TODO: clean up \U0001F4A9 and write docsting"""
    pass


# @_snoop
def main(url: str = None) -> None:
    """Parse and save"""
    handler = _load_page(url or URL)
    parsed = _parse(handler.data)
    _save_result(parsed)


if is_script:
    print("\033[0;32mHello from test_template.parser!\033[0m")
    main()
