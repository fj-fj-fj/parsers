# mypy: disable-error-code=attr-defined
import json as _json
from collections import defaultdict as _defaultdict
from time import time as _time
from typing import Any as _Any
from typing import NamedTuple as _NamedTuple
from typing import no_type_check as _no_type_check

import requests as _requests
from requests import Response as _Response
from bs4 import BeautifulSoup as _BeautifulSoup
from requests.exceptions import JSONDecodeError as _JSONDecodeError

from parsers.constants import Constant as _Constant
from parsers.datatypes import union_html_soup_json as _union_html_soup_json
from parsers.storage.files import ContextStorage as _ContextStorage
from parsers.storage.files import File as _File


class HandledData(_NamedTuple):
    """Encapsulates handled data and an error indicator"""
    data: _union_html_soup_json
    fail: bool
    status_code: int

    def __repr__(self) -> str:
        """HandledData(data=HTML|bs4|json, fail=False|True)"""
        data, fail, status_code = self.__rdata(), self.fail, self.status_code
        return f'{self.__class__.__name__}({data=}, {fail=}, {status_code=})'

    @_no_type_check
    def __rdata(self):
        assert self.data, f'Handled data cannot by empty. {self.data!r}'
        match self.data:
            case str():
                lines = len(self.data.splitlines())
                data = f'<!DOCTYPE html [{lines=}]>'
            case _BeautifulSoup():
                data = _BeautifulSoup
            case _:
                data = type(self.data)
        return data

class RequestHandler:

    def __init__(self):
        self._server_response = None
        self.url = None
        self.ct = None

    @property
    def response(self):
        print(f'Request {self.url}...')
        return self._make_request()

    def _make_request(self, url: str = None):
        self.server_response = _requests.get(url or self.url)
        self.ct = self.server_response.headers.get('Content-Type', '')
        return self.server_response

    @property
    def server_response(self):
        return self._server_response

    @server_response.setter
    def server_response(self, response):
        self._server_response = response

    @property
    def content_data_type(self):
        return 'json' if self.is_json() else 'str'

    def is_json(self) -> bool:
        return 'application/json' in self.ct


class DataHandler:

    def __init__(self):
        self._raw = None
        self._soup = None
        self._parsed = []
        self.is_json = False
        self.samples = None
        self.sample_handler = None
        self.handled_data = None

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, response):
        try:
            self.is_json = True
            self._raw = response.json()
            print('Data contains json')
        except _JSONDecodeError:
            self.is_json = False
            self.soup = response.text
            print('Data contains text')

    @property
    def soup(self):
        return self._soup

    @soup.setter
    def soup(self, raw):
        if not self.is_json:
            self._soup = _BeautifulSoup(raw, _Constant.PARSE.PARSER)

    def prepare(self):
        if not self.samples:
            return self.raw if self.is_json else self.soup
        # assert self.raw is not None
        # if self.is_json:
        #     keychain = self.raw
        #     for key in keychain.split('.'):
        #         keychain = keychain.get(key, 'chain_none')
        #     return keychain
        print(f'Sample:\n\t{self.samples}')
        print(f'Sample handler: {self.sample_handler}')
        assert self.soup is not self.sample_handler is not None
        for sample in self.samples:
            self._parsed.append([s.text for s in self.soup.select(sample)])
        return _json.dumps(self.sample_handler(*self._parsed))

    @property
    def data(self):
        print('Preparing ...')
        return self.prepare()


class Handler:

    def __init__(self, url, parsed_dir, samples):
        """Return nu Handler object with spesified `url`, `parsed_dir`"""
        self._url = url
        self._parsed_dir = parsed_dir
        self._request_handler = RequestHandler()
        self._data_handler = DataHandler()
        self._context_storage = _ContextStorage()
        self.samples = samples
        self.logic = None

    @property
    def samples(self):
        return self._samples or self._samples.read()

    @samples.setter
    def samples(self, data):
        self._samples = data

    @samples.deleter
    def samples(self):
        self._samples.clear()

    def _request(self) -> _Response:
        return self.response

    @property
    def response(self) -> _Response:
        self._request_handler.url = self._url
        return self._request_handler.response

    @property
    def data(self) -> HandledData:
        self._interpret_data()
        self._data_handler.samples = self.samples
        self._data_handler.sample_handler = self.logic
        return HandledData(
            data=self._data_handler.data,
            fail=not self._request_handler.server_response.ok,
            status_code=0)

    def _interpret_data(self):
        self._data_handler.raw = self.prepare()

    def prepare(self) -> _Response | _File:
        if (response := self._request_handler.server_response) is not None:
            return response
        elif (file := _File.check(self._parsed_dir)) is not None:
            return file
        self._request()
        return self.prepare()

    @property
    def saved(self) -> int:
        assert self._request_handler.server_response, 'requests.get?'
        return self._context_storage\
            .map(self._request_handler.content_data_type)\
            .current(self._parsed_dir)\
            .save(self._request_handler.server_response.text)


class Parser:
    """Provides the parsing process core functionality.

    States:
        `_`: `requust._`: `parse._`: `save._`:
            Represent the last returned values

    Behavior:
        `go`: property
            Encapsulate the program's primary behavior
        `request(url=None)`:
            Make request and return response
        `parse`:
            Fetch raw and return json or soup or raw
        `save`:
            Save data to Constant.DIR.PARSED_DATA
        `last_result`:
            Contains last exp result
        `help(arg=None)`:
            Print doc about arg or list all attrs

    Interactive mode example:
        >>> parser = Parser('http://httpbin.org', '.')
        >>> parser.request()
        <Response [200]>
        >>> parser.parse()
        HandledData(data="<class 'bs4.BeautifulSoup'>", fail=False)
        >>> soup = _.data
        >>> # soup.select(<css selector string>)

    """
    _: _Response | HandledData | int = None

    def __init__(self, url: str, parsed_dir: str, samples: list):
        """Pass params to Handler and return nu Parser object.

        `called`:
            defaultdict updated dynamically after method calls.
            key: <method name>, value: epoch (float)
        `handler`:
            Initialized Handler with spesified `url`, `parsed_dir`
        `logic`:
            None by default. Takes a samples handler function

        """
        self.called: _defaultdict = _defaultdict(lambda: .0)
        self.handler = Handler(url, parsed_dir, samples)
        self.parsed: HandledData = None
        self.logic = None

    # def __getattribute__(self, __name: str) -> _Any:
    #     # map __name with Man.names and print help msg

    @property
    def go(self) -> HandledData:
        """Encapsulate the program's primary behavior"""
        if not self.called['request']:
            self.request()
        if not self.called['parse']:
            self.parse()
        if not self.called['parse']:
            self.save()
        return Parser.parse._

    def request(self, url: str = None) -> _Response:
        """Make request and return response"""
        if url:
            self.handler._url = url
        self._ = Parser.request._ = self.handler.response
        self.called['request'] = _time()
        return Parser.request._

    def parse(self) -> HandledData:
        """Fetch raw and return json or soup"""
        self.handler.logic = self.logic
        self._ = Parser.parse._ = self.handler.data
        self.called['parse'] = _time()
        return Parser.parse._

    def save(self) -> int:
        """Save data to Constant.DIR.PARSED_DATA"""
        self._ = Parser.save._ = self.handler.saved
        self.called['save'] = _time()
        return Parser.save._

    @property
    def last_result(self) -> _Any:
        """Represent the last returned value"""
        return self._

    def help(self, act: str = None) -> None:
        """Print doc about `act` or list all public attrs"""
        if act is not None:
            return print(getattr(self, act).__doc__)
        print('\n'.join(m for m in dir(self) if not m.startswith('_')))
