#!/usr/bin/env python
# flake8: noqa F821
__all__ = 'Constant',

import typing as _t
from enum import Enum as _Enum
from os import getenv as _getenv

if is_script := __name__ == '__main__':
    from sys import path as _path
    from os.path import dirname as _dn
    _path.append(_dn(_dn(__file__)))

from parsers.datatypes import classproperty as _classproperty
from parsers.exceptions import ParameterValueError as _ParameterValueError

_NamespaceLiteral = _t.Literal[
    'cli',
    'dir',
    'file',
    'url',
    'parse',
    'prompt',
    'magic_numbers',
    'timeouts'
]

_ALL_OR_NS = _t.Literal['all', 'ns']

_PROJECT_DIR: _t.Final = _getenv('PROJECT_DIR', '../..')
_PROXY_DATA_DIR: _t.Final = F'{_PROJECT_DIR}/data/proxy/'


class _CommandLineInterface(_Enum):
    PARSE: _t.Final = '--parse'
    VERBOSE: _t.Final = '--verbose'


class _NameSpace(_t.NamedTuple):

    def __repr__(self) -> str:
        attributes = ', '.join(
            f"{attr}='{getattr(self, attr)}'" for attr in dir(self)
            if attr.isupper()
        )
        return f'{self.__class__.__name__}({attributes})'


class _Directories(_NameSpace):
    PARSED_DATA: _t.Final = F'{_PROJECT_DIR}/data/'
    LOG: _t.Final = F'{_PROJECT_DIR}/log/'
    PARSERS: _t.Final = F'{_PROJECT_DIR}/parsers/'
    USER_PARSERS: _t.Final = F'{_PROJECT_DIR}/parsers/user_parsers/'


class _Files(_NameSpace):
    # proxy
    PROXY_RESPONSE: _t.Final = F'{_PROXY_DATA_DIR}response.html'
    PARSED_PROXIES: _t.Final = F'{_PROXY_DATA_DIR}proxies'
    VALID_PROXIES: _t.Final = F'{_PROXY_DATA_DIR}valid'
    INVALID_PROXIES: _t.Final = F'{_PROXY_DATA_DIR}invalid'
    # useragent
    USER_AGENTS: _t.Final = F'{_PROJECT_DIR}/useragents.txt'
    # xpath general file
    SAMPLE: _t.Final = F'{_PROJECT_DIR}/samples.txt'
    NOTES: _t.Final = F'{_PROJECT_DIR}/notes.txt'
    # log files
    DEBUG_OUT = F'{_PROJECT_DIR}/log/out.log'
    DEBUG_ERR = F'{_PROJECT_DIR}/log/err.log'
    DEBUG_ALL = F'{_PROJECT_DIR}/log/all.log'


class _Prompt(_NameSpace):
    ENTER_URL_OR_FALSE: _t.Final = "Enter URL (or False to use 'httpbin.org'): "
    ENTER_BS4_PARSER: _t.Final = "Type enter to use 'lxml' or enter other:  "


class _MagicNumbers(_NameSpace):
    DEFAULT_CONNECTION_TIMEOUT: _t.Final = 5.05
    DEFAULT_READ_TIMEOUT: _t.Final = 27.67


class _ParsingConstants(_NameSpace):
    PARSER: _t.Final = 'lxml'
    # FOR: https://free-proxy-list.net/
    SELECT_IP = 'td:nth-of-type(1)'
    SELECT_PORT = 'td:nth-of-type(2)'


class _UniformResourceLocator(_NameSpace):
    # A simple HTTP Request & Response Service
    HTTPBIN_ORG: _t.Final = 'https://httpbin.org/'
    # proxies
    _FPL_PROXY_URL: _t.Final = 'https://free-proxy-list.net/'
    PROXY_URL = _FPL_PROXY_URL
    # checking
    CHECK_PROXY_URL: _t.Final = 'https://api.ipify.org/'
    CHECK_PROXY_URL_PARAMS: _t.Final = '{"format": "json"}'


class _DirAttributesMixin:
    """Mixin to listing namespaces and/or their constatns"""

    @classmethod
    def dir(cls, namespace: _NamespaceLiteral) -> str:
        """Return public _ConstantStorage.<namespace>.constants"""
        try:
            namespace = dir(vars(cls)[namespace.upper()].fget(cls))  # type: ignore [assignment]
            return ', '.join(const for const in namespace if const.isupper())
        except KeyError:
            raise _ParameterValueError(f'{namespace} not in {_NamespaceLiteral}')

    @classmethod
    def dir_public(cls, key: _ALL_OR_NS = 'all') -> str:
        r"""Return all public constants or thier namespases only"""
        constants_ns_map = {
            'all': ''.join(f'{ns}: {cls.dir(ns)}\n' for ns in dir(cls) if ns.isupper()),  # type: ignore [arg-type]
            'ns': ', '.join(ns for ns in dir(cls) if ns.isupper()),
        }
        try:
            return constants_ns_map[key]
        except KeyError:
            raise _ParameterValueError(f"'key' is a {_ALL_OR_NS}")


class _ConstantStorage(_DirAttributesMixin):

    @_classproperty
    def CLI(cls): return _CommandLineInterface      # noqa: E704

    @_classproperty
    def DIR(cls): return _Directories()             # noqa: E704

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


assert not (symmetric_difference := set(
    {ns.lower() for ns in _ConstantStorage.dir_public('ns').split(', ')}
    ^ {v for v in _NamespaceLiteral.__args__}  # type: ignore [attr-defined]
)), f"{symmetric_difference=}  '_ConstantStorage.dir_public' != '_NamespaceLiteral'"
del symmetric_difference


@_t.final
class Constant(_ConstantStorage):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({_ConstantStorage.dir_public('ns')})"
