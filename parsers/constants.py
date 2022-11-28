#!/usr/bin/env python
"""Module 'constants' that contains request constants."""

__all__ = 'ConstantStorage',

from enum import Enum
from os import getenv
from typing import Literal
from typing import NamedTuple

if is_script := __name__ == '__main__':
    from sys import path; from os.path import dirname  # noqa: E702
    path.append(dirname(dirname(__file__)))

from parsers.datatypes import classproperty
from parsers.datatypes import NamespaceLiteral
from parsers.exceptions import ParameterValueError

PROJECT_DIR = getenv('PROJECT_DIR', '../..')
PROXY_DATA = F'{PROJECT_DIR}/data/proxy'


class CommandLineInterface(Enum):
    PARSE = '--parse'
    VERBOSE = '--verbose'


class NameSpace(NamedTuple):
    """Base class for all namespaces."""


class Files(NameSpace):
    PARSED_DATA = F'{PROXY_DATA}/data'
    # proxy
    PROXY_RESPONSE = F'{PROXY_DATA}/response.html'
    PARSED_PROXIES = F'{PROXY_DATA}/proxies'
    VALID_PROXIES = F'{PROXY_DATA}/valid'
    INVALID_PROXIES = F'{PROXY_DATA}/invalid'
    # useragent
    USER_AGENTS = F'{PROJECT_DIR}/useragents.txt'


class MagicNumbers(NameSpace):
    DEFAULT_CONNECTION_TIMEOUT = 5.05
    DEFAULT_READ_TIMEOUT = 27.67


class ParsingConstants(NameSpace):
    PARSER = 'lxml'
    # FOR: https://free-proxy-list.net/
    SELECT_IP = 'td:nth-of-type(1)'
    SELECT_PORT = 'td:nth-of-type(2)'


class UniformResourceLocator(NameSpace):
    # proxies
    FPL_PROXY_URL = 'https://free-proxy-list.net/'
    PROXY_URL = FPL_PROXY_URL
    # checking
    CHECK_PROXY_URL = 'https://api.ipify.org/'
    CHECK_PROXY_URL_PARAMS = {'format': 'json'}


class DirAttributesMixin:
    """Mixin to listing namespaces and/or their constatns."""

    @classmethod
    def dir(cls, namespace: NamespaceLiteral) -> str:
        """Return public ConstantStorage.<namespace>.constants

        >>> ConstantStorage().dir('cli')
        'PARSE, VERBOSE'
        >>> ConstantStorage().dir('file')
        'INVALID_PROXIES, PARSED_PROXIES, PROXY_RESPONSE, USER_AGENTS, VALID_PROXIES'
        >>> ConstantStorage().dir('magic_numbers')
        'DEFAULT_CONNECTION_TIMEOUT, DEFAULT_READ_TIMEOUT'
        >>> ConstantStorage().dir('parse')
        'PARSER, SELECT_IP, SELECT_PORT'
        >>> ConstantStorage().dir('timeouts')
        ''
        >>> ConstantStorage().dir('url')
        'CHECK_PROXY_URL, CHECK_PROXY_URL_PARAMS, FPL_PROXY_URL'
        >>> ConstantStorage().dir('foo')  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        exceptions.ParameterValueError: foo not in \
typing.Literal['cli', 'file', 'url', 'parse', 'magic_numbers', 'timeouts']

        """
        try:
            namespace = dir(vars(cls)[namespace.upper()].fget(cls))  # type: ignore [assignment]
            return ', '.join(const for const in namespace if const.isupper())
        except KeyError:
            raise ParameterValueError(f'{namespace} not in {NamespaceLiteral}')

    @classmethod
    def dir_public(cls, key: Literal['all', 'ns'] = 'all') -> str:
        r"""Return all public constants or thier namespases only.

        >>> ConstantStorage().dir_public()  # doctest: +ELLIPSIS
        'CLI: PARSE, VERBOSE\nFILE: ...\nPARSE: ...\nURL: ...\n'
        >>> ConstantStorage().dir_public('ns')
        'CLI, FILE, MAGIC_NUMBERS, PARSE, TIMEOUTS, URL'
        >>> ConstantStorage().dir_public('badparam')
        Traceback (most recent call last):
        ...
        exceptions.ParameterValueError: 'what' is a Literal['all', 'ns'].

        """
        constants_ns_map = {
            'all': ''.join(f'{ns}: {cls.dir(ns)}\n' for ns in dir(cls) if ns.isupper()),  # type: ignore [arg-type]
            'ns': ', '.join(ns for ns in dir(cls) if ns.isupper()),
        }
        try:
            return constants_ns_map[key]
        except KeyError:
            raise ParameterValueError("'what' is a Literal['all', 'ns'].")


class ConstantStorage(DirAttributesMixin):
    """Contains classmethod-properties (files, URLs, xpath, etc)."""

    @classproperty
    def CLI(cls): return CommandLineInterface      # noqa: E704

    @classproperty
    def FILE(cls): return Files()                  # noqa: E704

    @classproperty
    def URL(cls): return UniformResourceLocator()  # noqa: E704

    @classproperty
    def PARSE(cls): return ParsingConstants()      # noqa: E704

    @classproperty
    def MAGIC_NUMBERS(cls): return MagicNumbers()  # noqa: E704

    @classproperty
    def TIMEOUTS(cls) -> tuple[float, float]:
        """Return default timeouts."""
        mn = ConstantStorage.MAGIC_NUMBERS
        return mn.DEFAULT_CONNECTION_TIMEOUT, mn.DEFAULT_READ_TIMEOUT


def info() -> None:
    """Display detail imformation about 'constants' module."""
    msg = f'{__doc__}\n\n'
    msg += '<ConstantStorage> contains (namespase: constants):\n'
    msg += f'{ConstantStorage.dir_public()}'
    print(msg)


if is_script:
    info()
