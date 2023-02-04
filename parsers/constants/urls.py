__all__ = [
    'HTTPBIN_ORG',
    'CHECK_PROXY_URL',
    'CHECK_PROXY_URL_PARAMS',
    'URL',
]
import typing as _t

# A simple HTTP Request & Response Service
HTTPBIN_ORG = 'https://httpbin.org/'

CHECK_PROXY_URL = 'https://api.ipify.org/'
CHECK_PROXY_URL_PARAMS = '{"format": "json"}'


class URL(_t.NamedTuple):
    HTTPBIN_ORG: str = HTTPBIN_ORG
    CHECK_PROXY_URL: str = CHECK_PROXY_URL
    CHECK_PROXY_URL_PARAMS: str = CHECK_PROXY_URL_PARAMS
