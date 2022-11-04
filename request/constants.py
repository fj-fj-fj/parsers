"""Contains constants."""

__all__ = 'CONSTANTS',

from collections import namedtuple
from types import SimpleNamespace

from utils import classproperty


_FileSimpleNamespace = SimpleNamespace(
    RESPONSE_PROXY='request/proxy/log/response.html',
    PARSED_PROXIES='request/proxy/parsed_data/proxies',
    VALID_PROXIES='request/proxy/parsed_data/valid',
    INVALID_PROXIES='request/proxy/parsed_data/invalid',

    USER_AGENTS='request/useragent/user_agents.txt',
)


_MagicNumbersSimpleNamespace = SimpleNamespace(
    default_timeout=namedtuple('default_timeout',
        field_names=['CONNECTION_TIMEOUT', 'READ_TIMEOUT'],
        defaults=[5.05, 27.77],
    ),
)

_SpiderSimpleNamespace = SimpleNamespace(
    # FOR: https://free-proxy-list.net/
    SELECT_IP='td:nth-of-type(1)',
    SELECT_PORT='td:nth-of-type(2)',
)


_URLSimpleNamespace = SimpleNamespace(
    FPL_PROXY_URL='https://free-proxy-list.net/',

    CHECK_PROXY_URL='https://api.ipify.org/',
    CHECK_PROXY_URL_PARAMS={'format': 'json'},
)


class CONSTANTS:
    """
    Contains classmethod-properties (files, URLs, xpath, etc).

    dir_public(): classmethod to check public namespaces
    dir(namespace: str): classmethod to check namespace's constants

    """
    @classproperty
    def FILE(cls):
        return _FileSimpleNamespace

    @classproperty
    def URL(cls):
        return _URLSimpleNamespace

    @classproperty
    def SPIDER(cls):
        return _SpiderSimpleNamespace

    @classproperty
    def MAGIC_NUMBERS(cls):
        return _MagicNumbersSimpleNamespace

    @classproperty
    def TIMEOUT(cls):
        """Return default timeout as namedtuple[float, float]"""
        return CONSTANTS.MAGIC_NUMBERS.default_timeout()

    @classproperty
    def dir_public(cls) -> str:
        """Return public namespaces"""
        return ', '.join(ns for ns in dir(cls) if ns.isupper())

    @classmethod
    def dir(cls, namespace) -> str:
        """Return public CONSTANTS.<namespace>.constants"""
        namespace = dir(vars(cls)[namespace.upper()].fget(cls))
        return ', '.join(const for const in namespace if const.isupper())
