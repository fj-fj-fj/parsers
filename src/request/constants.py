#!/usr/bin/env python
"""Module 'constants' that contains request constants."""

__all__ = 'ConstantStorage',

from enum import Enum
from typing import Literal
from typing import NamedTuple

if is_script := __name__ == '__main__':
    from sys import path; from os.path import dirname  # noqa: E702
    path.append(dirname(dirname(__file__)))

from utils import classproperty

PWD = __file__.rsplit('/', 1)[0]


class CommandLineInterface(Enum):
    PARSE = '--parse'
    VERBOSE = '--verbose'


class Files(NamedTuple):
    # proxy files
    PROXY_RESPONSE: str = f'{PWD}/proxy/log/response.html'
    PARSED_PROXIES: str = f'{PWD}/proxy/parsed_data/proxies'
    VALID_PROXIES: str = f'{PWD}/proxy/parsed_data/valid'
    INVALID_PROXIES: str = f'{PWD}/proxy/parsed_data/invalid'
    # useragent files
    USER_AGENTS: str = f'{PWD}/useragent/user_agents.txt'


class MagicNumbers(NamedTuple):
    DEFAULT_CONNECTION_TIMEOUT: float = 5.05
    DEFAULT_READ_TIMEOUT: float = 27.67


class ParsingConstants(NamedTuple):
    PARSER: str = 'lxml'
    # FOR: https://free-proxy-list.net/
    SELECT_IP: str = 'td:nth-of-type(1)'
    SELECT_PORT: str = 'td:nth-of-type(2)'


class UniformResourceLocator(NamedTuple):
    # proxies
    FPL_PROXY_URL: str = 'https://free-proxy-list.net/'
    # checking
    CHECK_PROXY_URL: str = 'https://api.ipify.org/'
    CHECK_PROXY_URL_PARAMS: dict[str, str] = {'format': 'json'}


class ConstantStorage:
    """
    Contains classmethod-properties (files, URLs, xpath, etc).

    dir_public(): classmethod to check public namespaces
    dir(namespace: str): classmethod to check namespace's constants

    """
    @classproperty
    def CLI(cls): return CommandLineInterface    # noqa: E704

    @classproperty
    def FILE(cls): return Files                  # noqa: E704

    @classproperty
    def URL(cls): return UniformResourceLocator  # noqa: E704

    @classproperty
    def PARSE(cls): return ParsingConstants      # noqa: E704

    @classproperty
    def MAGIC_NUMBERS(cls): return MagicNumbers  # noqa: E704

    @classproperty
    def TIMEOUTS(cls) -> tuple[float, float]:
        """Return default timeouts."""
        mn = ConstantStorage.MAGIC_NUMBERS
        return mn.DEFAULT_CONNECTION_TIMEOUT, mn.DEFAULT_READ_TIMEOUT

    @classmethod
    def _dir(cls, namespace: str) -> str:
        """Return public ConstantStorage.<namespace>.constants"""
        namespace = dir(vars(cls)[namespace.upper()].fget(cls))
        return ', '.join(const for const in namespace if const.isupper())

    @classmethod
    def _dir_public(cls, what: Literal['all', 'ns'] = 'all') -> str:
        """Return all public constants or thier namespases only."""
        return {
            'all': ''.join(f"{ns}: {cls._dir(ns)}\n" for ns in dir(cls) if ns.isupper()),
            'ns': ', '.join(ns for ns in dir(cls) if ns.isupper()),
        }.get(what, "ParameterError: `what` is Literal['all', 'ns'].")


def info():
    """Display detail imformation about this module."""
    msg = f'{__doc__}\n\n'
    msg += '<ConstantStorage> contains (namespase: constants):\n'
    msg += f'{ConstantStorage._dir_public()}'
    print(msg)


if is_script:
    info()
    c = ConstantStorage  # if -i
