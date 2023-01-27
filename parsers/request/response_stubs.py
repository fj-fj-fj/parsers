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
            self.__content_type = _Sequence.__name__
        elif isinstance(__r, _Mapping):
            self._content = json.dumps(dict(__r)).encode()
            self.__content_type = _Mapping.__name__
        else:
            # Indicate __r requires non-text and non-json logic
            self._content = None
            self.__content_type = self.__r.__class__.__name__

        # FIXME: check status_code
        self._ok = isinstance(self._content, str)

    def __repr__(self):
        return self._make_repr()

    def _make_repr(self) -> str:
        cls = self.__r.__class__.__name__
        type = self.__content_type
        try:
            len = self.__r.__len__()
            return f"<{cls} [{type=}, {len=}]>"
        except AttributeError:
            return repr(self.__r)

    @property
    def ok(self) -> bool:
        return self._ok
