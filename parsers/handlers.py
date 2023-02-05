# flake8: noqa W503
# mypy: disable-error-code=attr-defined
import sys as _sys
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
from parsers.datatypes import fetch_values_by_keys as _fetch_values_by_keys
from parsers.datatypes import KeyAttrValue as _KeyAttrValue
from parsers.format.colors import Colors as _Colors
from parsers.imports import debugcls as _debugcls
from parsers.imports import warn_object_not_found as _warn_object_not_found
from parsers.request.response_stubs import NoAutoResponse as _NoAutoResponse
from parsers.storage.files import ContextStorage as _ContextStorage
from parsers.storage.files import File as _File


class HandledData(_t.NamedTuple):
    data: _Content.UNION_HTML_SOUP_JSON
    fail: str = None
    status_code: int = int(bool(fail))

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

    def __init__(self, *, get=_requests.get, url: str = None):
        # Response or NoAutoResponse
        self.server_response: _ResponseLike = None
        # Initial response object
        self.__r  = None
        # # Keep previous responses
        self._previous_responses: list[_ResponseLike] = []
        # requests.get or like
        self.get = get
        self.url = url
        self._validated_url: str = None

    @property
    def response(self) -> _Response:
        """Make request and return response or raise if not url"""
        assert self.url is not None
        return self._make_request(self.url)

    def _make_request(self, url: str = None):
        """Send a GET request to the web server"""
        self._keep_previous_response()
        self._validated_url = self.validate(url or self.url)
        # TODO: catch HTMLError, URLError
        self.__r = self.get(self._validated_url)
        self.server_response = self._make_response(self.__r)
        return self.server_response

    def _keep_previous_response(self) -> None:
        """Check previous response exists to save it"""
        if self.server_response is not None:
            self._previous_responses.append(self.server_response)

    def _make_response(self, __r) -> _ResponseLike:
        """If `self.get` is not default, `NoAutoResponse` will be returned"""
        return __r if isinstance(__r, _Response) else _NoAutoResponse(__r)

    def validate(self, url: str) -> str:
        """assert the URL scheme is valid.

        input() will be called if exist an empty braces in the URL.
        """
        assert (f:=url.startswith)('https://') or f('http://'), f'invalid {url=}'
        # TODO: str subclass, override __format__ (add color spec) ish
        empty_braces = f'{_Colors.RED}{{?}}{_Colors.NC}'
        prompt = f'{_Colors.RED}(Fix URL){_Colors.NC} >>> '
        incorrect_url_dialog = f'{url.format(empty_braces)}\n{prompt}'
        return url if '{}' not in url else url.format(input(incorrect_url_dialog))

    @property
    def isdefalut_response(self) -> bool:
        """requests.Response or not"""
        return self.__r.__class__.__name__ == _Response.__name__

    @property
    def get_default_response(self):
        return self.__r


@_debugcls
class DataHandler:

    def __init__(self, markup_parser=_Constant.PARSE.PARSERS.FASTEST):
        self.markup_parser = markup_parser
        # Direct access to data
        self.raw_content: _Content.HTML = None
        self.json: _Content.JSON = None
        self._soup: _BeautifulSoup = None
        self._soup_text = []
        self.final_data = None
        # Access to data by 'text' or 'json()'
        self.response_obj: _ResponseLike = None
        # Access to data by 'key_value' or 'attr_value'
        # TODO: merge HandledData with KeyAttrFinder ish
        self.key_attr_value: _KeyAttrValue = None

        # Data processing logic by samples
        self.sample_handler = None
        # Data processing criteria
        self.samples = None

        # flags
        self.is_json = None

    def clean_up(self) -> None:
        """Clear containers, set other attributes to None"""
        self.raw_content = self._soup = self.json = self.final_data =\
        self.response_obj = self.key_attr_value = self.sample_handler =\
        self.is_json = self.samples = self._soup_text.clear()

    @property
    def raw(self) -> _Content.UNION_SOUP_JSON | None:
        """Return the 1st true: `_soup`, `json`, `raw_content`"""
        return self._soup or self.json or self.raw_content

    @raw.setter
    def raw(self, response_obj: _ResponseLike) -> None:
        """Clean up and try to make json or soup from `response_obj`"""
        self.clean_up()
        self.response_obj = response_obj
        self.raw_content = response_obj.text
        try:
            self.json = response_obj.json()
            self.is_json = True
        except _JSONDecodeError:
            # raw_content is an empty str or None
            if not self.raw_content:
                return
            # Make soup
            self.soup = self.raw_content
            self.is_json = False

    @property
    def soup(self) -> _BeautifulSoup | None:
        return self._soup

    @soup.setter
    def soup(self, markup: str | _t.IO) -> None:
        """Make `BeautifulSoup` from `markup` with `self.markup_parser`"""
        self._soup = _BeautifulSoup(markup, self.get_markup_parser())

    def get_markup_parser(self) -> str:  # current or built-in
        """Try to return `self.markup_parser` or setup (and return) builtin"""
        try:
            self.markup_parser = __import__(self.markup_parser).__name__
        except ModuleNotFoundError:
            _warn_object_not_found(self.markup_parser)
            self.markup_parser = _Constant.PARSE.PARSERS.BUILTIN
        return self.markup_parser

    @property
    def data(self) -> _Content.UNION_HTML_SOUP_JSON:
        """Return the 1st true: `final_data`, `json`, `soup`, `raw_content`"""
        return self.raw if _sys.flags.interactive else self._prepare()

    def _prepare(self):
        """Process `sample_handler` and return `final_data`"""
        # State: soup
        # Process with samples (css or xpath)
        if self.soup and self.samples and self.sample_handler:
            # TODO: pass it into logic.py
            for sample in self.samples:
                self._soup_text.append([s.text for s in self.soup.select(sample)])
            self.final_data = self.sample_handler(self._soup_text)
            self.is_json = isinstance(self.final_data, (list, dict))

        # State: json as list
        # Process directly (without samples)
        # TODO: samples is a groupby criteria ish
        elif not self.samples and self.json and self.sample_handler:
            self.final_data = self.sample_handler(self.json)

        # State: json as dict or Response is not requests.Response
        # Process with samples throw fetch_values_by_keys()
        # TODO: if json is None fetch attr_value else key_value ish
        elif self.samples and self.sample_handler:
            self.key_attr_value = self.find_samples()
            self.final_data = self.sample_handler(self.key_attr_value)

        else:
            assert False, self.__dict__
        return self.final_data

    def find_samples(self) -> _KeyAttrValue:
        return _fetch_values_by_keys(
            keypath=self.samples,
            # if samples contain keypath(s)
            data=self.json,
            # if samples contain attribute(s)
            obj=self.response_obj,
        )

    @property
    def step(self) -> _t.Literal[2, 1, 0]:
        """Map {final_data: 2, _soup or json: 1, raw_data: 0}"""
        return 2 if self.final_data else 1 if self._soup or self.json else 0


@_debugcls
class Handler:
    """Manager for RequestHandler, DataHandler, ContextStorage.

    Base API:
        response (property):
            (with RequestHandler) return server response
        parsed (property):
            (with DataHandler) return HandledData
        save()
            (with ContextStorage) return int saved chars

    """
    def __init__(self, url: str, parsed_dir: str):
        self.parsed_dir = parsed_dir
        self.url = url
        self.sample_handler = None
        self.request_handler = RequestHandler()
        self.data_handler = DataHandler()
        self.context_storage = _ContextStorage()

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
        self.request_handler.url = self.url
        res = self.request_handler.response
        self.save()  # raw_content
        return res

    @property
    def parsed(self) -> HandledData:
        self._prepare()
        # TODO: error = self._prepare()
        #       pass `error`(str | None) to `HandledData` as `fail`
        return HandledData(data=self.data_handler.data)

    def _prepare(self) -> None:
        # TODO: text property and json() for not-default response ish
        # Extract data from response
        self.data_handler.raw = self.get_response_or_read_file()
        # Pass logic and criteria to process data
        self.data_handler.samples = self.samples
        self.data_handler.sample_handler = self.sample_handler
        self.save()  # intermediate (_soup or json)

    def get_response_or_read_file(self) -> _ResponseLike:
        if (response := self.request_handler.server_response) is not None:
            return response
        # Parse data from file
        elif (file := _File.check(self.parsed_dir)) is not None:
            return file
        assert False, self.__dict__

    def save(self) -> int:
        """Save current data with current storage"""
        return (
            # Manager storage
            self.context_storage
                .map(datatype=self.current_storage)
            # Worker storage
                .current(parsed_dir=self.parsed_dir)
                .save(data=self.current_data, step=self.data_handler.step)
        )  # Implemented workers: PlainStorage, JsonStorage

    @property
    def current_storage(self):
        return ('str', 'json')[bool(self.data_handler.is_json)]

    @property
    def current_data(self) -> _Content.UNION_HTML_JSON | str:
        """Return any: final_data, soup, json, response.text, response name"""
        return (
            self.data_handler.final_data
            or self.data_handler.json
            or (soup := self.data_handler.soup) and str(soup)
            or (resp := self.request_handler.server_response) and resp.text
            or resp.__class__.__name__
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
            Initialized Sample
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
        self._ = Parser.parse._ = self.handler.parsed
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
