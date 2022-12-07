#!/usr/bin/env python
# flake8: noqa F821
"""The 'constants' module contains request constants."""

__all__ = 'Constant',

from enum import Enum as _Enum
from os import getenv as _getenv
from typing import Literal as _Literal
from typing import NamedTuple as _NamedTuple

if is_script := __name__ == '__main__':
    from sys import path as _path
    from os.path import dirname as _dn
    _path.append(_dn(_dn(__file__)))

from parsers.datatypes import classproperty as _classproperty
from parsers.exceptions import ParameterValueError as _ParameterValueError

_NamespaceLiteral = _Literal[
    'cli',
    'dir',
    'file',
    'url',
    'parse',
    'prompt',
    'magic_numbers',
    'timeouts'
]

_ALL_OR_NS = _Literal['all', 'ns']


_PROJECT_DIR = _getenv('PROJECT_DIR', '../..')
_PROXY_DATA_DIR = F'{_PROJECT_DIR}/data/proxy/'


class _CommandLineInterface(_Enum):
    PARSE = '--parse'
    VERBOSE = '--verbose'


class _NameSpace(_NamedTuple):
    """Base class for all namespaces."""


class _Directories(_NameSpace):
    PARSED_DATA = F'{_PROJECT_DIR}/data/'
    PARSERS = F'{_PROJECT_DIR}/parsers/'
    USER_PARSERS = F'{_PROJECT_DIR}/parsers/user_parsers/'


class _Files(_NameSpace):
    # proxy
    PROXY_RESPONSE = F'{_PROXY_DATA_DIR}response.html'
    PARSED_PROXIES = F'{_PROXY_DATA_DIR}proxies'
    VALID_PROXIES = F'{_PROXY_DATA_DIR}valid'
    INVALID_PROXIES = F'{_PROXY_DATA_DIR}invalid'
    # useragent
    USER_AGENTS = F'{_PROJECT_DIR}useragents.txt'


class _Prompt(_NameSpace):
    ENTER_URL_OR_FALSE = "Enter URL (or False to use 'httpbin.org'): "
    ENTER_BS4_PARSER = "Type enter to use 'lxml' or enter other:  "


class _MagicNumbers(_NameSpace):
    DEFAULT_CONNECTION_TIMEOUT = 5.05
    DEFAULT_READ_TIMEOUT = 27.67


class _ParsingConstants(_NameSpace):
    PARSER = 'lxml'
    # FOR: https://free-proxy-list.net/
    SELECT_IP = 'td:nth-of-type(1)'
    SELECT_PORT = 'td:nth-of-type(2)'


class _UniformResourceLocator(_NameSpace):
    # A simple HTTP Request & Response Service
    HTTPBIN_ORG = 'https://httpbin.org/'
    # proxies
    FPL_PROXY_URL = 'https://free-proxy-list.net/'
    PROXY_URL = FPL_PROXY_URL
    # checking
    CHECK_PROXY_URL = 'https://api.ipify.org/'
    CHECK_PROXY_URL_PARAMS = {'format': 'json'}


class _DirAttributesMixin:
    """Mixin to listing namespaces and/or their constatns."""

    @classmethod
    def dir(cls, namespace: _NamespaceLiteral) -> str:
        """Return public _ConstantStorage.<namespace>.constants

        >>> _ConstantStorage().dir('cli')
        'PARSE, VERBOSE'
        >>> _ConstantStorage().dir('dir')
        'PARSED_DATA, PARSERS, USER_PARSERS'
        >>> _ConstantStorage().dir('file')
        'INVALID_PROXIES, PARSED_PROXIES, PROXY_RESPONSE, USER_AGENTS, VALID_PROXIES'
        >>> _ConstantStorage().dir('magic_numbers')
        'DEFAULT_CONNECTION_TIMEOUT, DEFAULT_READ_TIMEOUT'
        >>> _ConstantStorage().dir('parse')
        'PARSER, SELECT_IP, SELECT_PORT'
        >>> _ConstantStorage().dir('prompt')
        'ENTER_URL_OR_FALSE, ENTER_BS4_PARSER'
        >>> _ConstantStorage().dir('timeouts')
        ''
        >>> _ConstantStorage().dir('url')
        'CHECK_PROXY_URL, CHECK_PROXY_URL_PARAMS, FPL_PROXY_URL'
        >>> _ConstantStorage().dir('foo')  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        exceptions.ParameterValueError: foo not in \
typing.Literal['cli', 'dir', 'file', 'url', 'parse', \
'prompt', 'magic_numbers', 'timeouts']

        """
        try:
            namespace = dir(vars(cls)[namespace.upper()].fget(cls))  # type: ignore [assignment]
            return ', '.join(const for const in namespace if const.isupper())
        except KeyError:
            raise _ParameterValueError(f'{namespace} not in {_NamespaceLiteral}')

    @classmethod
    def dir_public(cls, key: _ALL_OR_NS = 'all') -> str:
        r"""Return all public constants or thier namespases only.

        >>> _ConstantStorage().dir_public()  # doctest: +ELLIPSIS
        'CLI: PARSE, VERBOSE\nDIR: ...\nPARSE: ...\nURL: ...\n'
        >>> _ConstantStorage().dir_public('ns')
        'CLI, DIR, FILE, MAGIC_NUMBERS, PARSE, PROMPT, TIMEOUTS, URL'
        >>> _ConstantStorage().dir_public('badparam')
        Traceback (most recent call last):
        ...
        exceptions._: 'key' is a typing.Literal['all', 'ns'].

        """
        constants_ns_map = {
            'all': ''.join(f'{ns}: {cls.dir(ns)}\n' for ns in dir(cls) if ns.isupper()),  # type: ignore [arg-type]
            'ns': ', '.join(ns for ns in dir(cls) if ns.isupper()),
        }
        try:
            return constants_ns_map[key]
        except KeyError:
            raise _ParameterValueError(f"'key' is a {_ALL_OR_NS}")


class _ConstantStorage(_DirAttributesMixin):
    """Contains classmethod-properties (files, URLs, xpath, etc)."""

    @_classproperty
    def CLI(cls): return _CommandLineInterface      # noqa: E704

    @_classproperty
    def DIR(cls): return _Directories()                  # noqa: E704

    @_classproperty
    def FILE(cls): return _Files()                  # noqa: E704

    @_classproperty
    def URL(cls): return _UniformResourceLocator()  # noqa: E704

    @_classproperty
    def PARSE(cls): return _ParsingConstants()      # noqa: E704

    @_classproperty
    def PROMPT(cls): return _Prompt()               # noqa: E704

    @_classproperty
    def MAGIC_NUMBERS(cls): return _MagicNumbers()  # noqa: E704

    @_classproperty
    def TIMEOUTS(cls) -> tuple[float, float]:
        """Return default timeouts."""
        mn = _ConstantStorage.MAGIC_NUMBERS
        return mn.DEFAULT_CONNECTION_TIMEOUT, mn.DEFAULT_READ_TIMEOUT


class Constant(_ConstantStorage):

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {_ConstantStorage.dir_public('ns')}>"
