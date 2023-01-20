__all__ = (
    'NoAutoResponse',
    'requests_get',
)
import json
from collections.abc import Sequence as _Sequence
from collections.abc import Mapping as _Mapping

from requests import Response as _Response

response_json = _Response()
response_json._content = b'[{"foo": true, "bar": false}]'

response_text = _Response()
response_text._content = b'foo, bar, egg, spam, lol'

_ResponseMock = _Response


def requests_get(return_json=False) -> _ResponseMock:
    return response_json if return_json else response_text


class NoAutoResponse(_Response):

    def __init__(self, __r):
        super().__init__()

        self.__r = __r
        if isinstance(__r, _Sequence):
            self._content = json.dumps(list(__r)).encode()
            self.__dtype = _Sequence.__name__
        elif isinstance(__r, _Mapping):
            self._content = json.dumps(dict(__r)).encode()
            self.__dtype = _Mapping.__name__
        else:
            self._content = __r.__str__().encode()
            if isinstance(__r, str):
                self.__dtype = str.__name__
            elif isinstance(__r, int):
                self.__dtype = int.__name__
            elif isinstance(__r, float):
                self.__dtype = float.__name__
            else:
                assert False, f'{self.__r}, {dir(self.__r)}'

        self._ok = self._content and True or False

    def __repr__(self):
        cls = self.__r.__class__.__name__
        type = self.__dtype
        len = self.__r.__len__()
        return f"<{cls} [{type=}, {len=}]>"

    @property
    def ok(self) -> bool:
        return self._ok
