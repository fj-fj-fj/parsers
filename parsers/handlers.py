# flake8: noqa W503
# mypy: disable-error-code=attr-defined
import typing as _t
from pprint import pprint as _pprint
from pydoc import pager as _pager
from time import time as _time
from collections import defaultdict as _defaultdict

import requests as _requests
from bs4 import BeautifulSoup as _BeautifulSoup
from requests import Response as _Response
from requests.exceptions import JSONDecodeError as _JSONDecodeError

from parsers.constants import Constant as _Constant
from parsers.datatypes import Content as _Content
from parsers.datatypes import ResponseLike as _ResponseLike
from parsers.datatypes import Sample as _Sample
from parsers.imports import debugcls as _debugcls
from parsers.storage.files import ContextStorage as _ContextStorage
from parsers.storage.files import File as _File


class HandledData(_t.NamedTuple):
    data: _Content.UNION_HTML_SOUP_JSON
    fail: bool
    status_code: int

    def __repr__(self):
        data, fail, status_code = self.__rdata(), self.fail, self.status_code
        return f'{self.__class__.__name__}({data=}, {fail=}, {status_code=})'

    @_t.no_type_check
    def __rdata(self):
        match self.data:
            case str():
                lines = len(self.data.splitlines())
                data = f'<!DOCTYPE html [{lines=}]>'
            case _BeautifulSoup():
                data = _BeautifulSoup
            case _:
                data = type(self.data)
        return data


@_debugcls
class RequestHandler:

    def __init__(self):
        self._server_response = None
        self._previous_responses = []
        self.url: str = None
        # self.ct: str = None

    @property
    def response(self) -> _Response:
        """Make request and return response"""
        assert self.url is not None
        return self._make_request(self.url)

    def _make_request(self, url: str = None):
        """Save previous response if it was and return new"""
        if self._server_response is not None:
            self._previous_responses.append(self._server_response)
        self.server_response = _requests.get(self.validate(url or self.url))
        self.ct = self.server_response.headers.get('Content-Type', '')
        return self.server_response

    @property
    def server_response(self):
        return self._server_response

    @server_response.setter
    def server_response(self, response: _Response) -> None:
        self._server_response = response

    @server_response.deleter
    def server_response(self) -> None:
        """Set previous response if it was. Set None if not"""
        if self._previous_responses:
            self._server_response = self._previous_responses.pop()
        self._server_response = None

    def validate(self, url: str) -> str:
        assert (f:=url.startswith)('https://') or f('http://'), f'invalid {url=}'
        return (
            url if '{}' not in url else
            url.format(input(f" {url.format('{ ? }')!r}\n\tfill placehoder: "))
        )


@_debugcls
class DataHandler:

    def __init__(self):
        self._soup: _BeautifulSoup = None
        self.json: _Content.JSON = None
        self.is_json = False
        self.handled_data = None
        self.samples = None
        self.sample_handler = None
        self._parsed = []
        self.final_data = None

    @property
    def step(self) -> _t.Literal[2, 1, 0]:
        """0: raw (page), 1: parsed (soup|json), 2: final"""
        return 2 if self.final_data else 1 if self._soup or self.json else 0

    @property
    def raw(self) -> _Content.UNION_SOUP_JSON | None:
        """Return parsed data (self.soup if exists else self.json)"""
        return self._soup or self.json

    @raw.setter
    def raw(self, response: _ResponseLike) -> None:
        """Set raw data(json|soup) from `response`"""
        try:
            self.json = response.json()
            self.is_json = True
        except _JSONDecodeError:
            self.is_json = False
            self.soup = response.text

    @property
    def soup(self) -> _BeautifulSoup:
        return self._soup

    @soup.setter
    def soup(self, raw: str) -> None:
        """Make soup from `raw` with `Constant.PARSE.PARSER`"""
        self._soup = _BeautifulSoup(raw, _Constant.PARSE.PARSER)

    @property
    def data(self):
        return self.prepare()

    def prepare(self) -> _Content.UNION_HTML_SOUP_JSON:
        """Return final data or intermediate (json|soup).

        For final data samples and/or sample handler must be created.
        Note: cook soup with select only (not select_one)
        """
        if not self.samples and not self.sample_handler:
            return self.json or self.soup

        assert self.sample_handler is not None

        if self.json is self.samples is self.sample_handler is None:
            self.final_data = self.raw
            return self.final_data
        elif self.json and self.sample_handler:
            self.final_data = self.sample_handler(self.json)
            return self.final_data

        # create [list[sample_result] for sample in samples]
        for sample in self.samples:
            self._parsed.append([s.text for s in self.soup.select(sample)])
        # GOTO: select or select_one
        self.final_data = self.sample_handler(self._parsed)
        self.is_json = True
        return self.final_data


@_debugcls
class Handler:
    """Manager for RequestHandler, DataHandler, ContextStorage.

    Base API:
        response (property):
            (with RequestHandler) return server response
        data (property):
            (with DataHandler) return HandledData
        save()
            (with ContextStorage) return int saved chars

    """
    def __init__(self, url: str, parsed_dir: str):
        self.parsed_dir = parsed_dir
        self.url = url
        self.sample_handler = None
        self._request_handler = RequestHandler()
        self._data_handler = DataHandler()
        self._context_storage = _ContextStorage()

    @property
    def samples(self) -> list[str]:
        return self._samples or self._samples.read()

    @samples.setter
    def samples(self, value: _Sample) -> None:
        self._samples = value

    @samples.deleter
    def samples(self) -> None:
        self._samples.save(truncate=True)
        self._samples.clear()

    @property
    def response(self) -> _Response:
        self._request_handler.url = self.url
        res = self._request_handler.response
        self.save()
        return res

    @property
    def data(self) -> HandledData:
        self._prepare()
        self.save()
        return HandledData(
            data=self._data_handler.data,
            fail=not bool(self._request_handler.server_response),
            status_code=0,
        )

    def _prepare(self) -> None:
        self._data_handler.raw = self._select_rawdata_object()
        self._data_handler.samples = self.samples
        self._data_handler.sample_handler = self.sample_handler

    def _select_rawdata_object(self) -> _ResponseLike:
        if (response := self._request_handler.server_response) is not None:
            return response
        elif (file := _File.check(self.parsed_dir)) is not None:
            return file
        self._request_handler.url = self.url
        return self._select_rawdata_object()

    @property
    def saved(self) -> _Content.UNION_HTML_SOUP_JSON:
        """Save and return current data"""
        self.save()
        return self.current_data

    def save(self) -> int:
        """Save current data with current storage"""
        return (
            # Manager storage
            self._context_storage
                .map(datatype=('str', 'json')[self._data_handler.is_json])
            # Worker storage
                .current(parsed_dir=self.parsed_dir)
                .save(data=self.current_data, step=self._data_handler.step)
        )

    @property
    def current_data(self) -> _Content.UNION_HTML_JSON | _t.Literal['None']:
        """Return final|parsed|HTML data or str(None)"""
        return (
            self._data_handler.final_data
            or self._data_handler.json
            or (soup := self._data_handler.soup) and str(soup)
            or (resp := self._request_handler.server_response) and resp.text
            or str(resp)
        )


@_debugcls
class Parser:
    """Provides the parsing process core functionality.

    States:
        `_`:
            The last returned value.
            Also: `request._`, `parse._`, `save._`

    Behavior:
        `go`: property
            Encapsulate the Parser primary behavior
        `request(url=None)`:
            Return Response or its-like object
        `parse()`:
            Extract data and return (json or soup) or page
        `less(text: str)`:
            `pydoc.pager` to emulate 'less' in repl
        `pp`:
            pprint.pprint
        `save()`:
            Save data to Constant.DIR.PARSED_DATA
        `last_result`: property
            Return the last returned value of the Parser object
        `help(method=None)`:
            Display `method` docstring or list all public

    """
    _: _Response | HandledData | int = None

    def __init__(self, url: str, parsed_dir: str, samples: _Sample):
        """Pass params to Handler and return nu Parser object.

        `handler`:
            Initialized Handler with spesified `url`, `parsed_dir`
        `samples`:
            Initialized Sample (empty if the mode is interactive)
        `logic()`:
            Sample handler function. None by default.

        """
        self.handler = Handler(url=url, parsed_dir=parsed_dir)
        self.less = lambda text: _pager(str(text))
        self.pp = _pprint
        # defaultdict updated dynamically after method calls.
        #   key(str): <method name>, value(float): epoch
        self._called: _defaultdict = _defaultdict(float)
        self.parsed: HandledData = None
        self.samples = samples
        self.logic = None

    # def __getattribute__(self, __name: str) -> _Any:
    #     # map __name with Man.names and print help msg

    @property
    def go(self) -> HandledData:
        """Encapsulate primary behavior (request|parse|save)"""
        if not self._called['request']:
            self.request()
        if not self._called['parse']:
            self.parse()
        self.save()
        return Parser.parse._

    def request(self, url: str = None) -> _Response:
        """Return Response or its-like object"""
        if url:
            self.handler.url = url
        self._ = Parser.request._ = self.handler.response
        self._called['request'] = _time()
        return Parser.request._

    def parse(self) -> HandledData:
        """Extract data and return (json or soup) or page"""
        self._preparse()
        self._ = Parser.parse._ = self.handler.data
        self._called['parse'] = _time()
        return Parser.parse._

    def _preparse(self) -> None:
        """Pass samples and data extracting logic to base Handler"""
        self.handler.samples = self.samples
        self.handler.sample_handler = self.logic

    def save(self) -> int:
        """Save data to Constant.DIR.PARSED_DATA"""
        self._ = Parser.save._ = self.handler.save()
        self._called['save'] = _time()
        return Parser.save._

    @property
    def last_result(self) -> _t.Any:
        """Return the last returned value of the Parser object"""
        return self._

    def help(self, method: str = None) -> None:
        """Display `method` docstring or list all public"""
        if method is not None:
            return print(getattr(self, method).__doc__)
        print('\n'.join(m for m in dir(self) if not m.startswith('_')))
