from requests import Response as _Response

response_json = _Response()
response_json._content = b'[{"foo": true, "bar": false}]'

response_text = _Response()
response_text._content = b'foo, bar, egg, spam, lol'

_ResponseMock = _Response


def requests_get(return_json=False) -> _ResponseMock:
    return response_json if return_json else response_text
