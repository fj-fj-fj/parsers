#!/usr/bin/env python
"""The 'core' module contains proxy parsers and checkers."""

from typing import Callable as _Callable

if is_script := __name__ == '__main__':
    def fix_path():
        '''Fix sys.path and disappear from the global scope.'''
        from sys import path; from os.path import dirname  # noqa: E702
        path.insert(0, dirname(dirname(dirname(dirname(__file__)))))
        global fix_path; del fix_path  # noqa: E702
    fix_path()

from parsers.request.proxy.checker import check
from parsers.request.proxy.checker import check_proxies
from parsers.request.proxy.parser import parse
from parsers.request.proxy.parser import parse_proxies


class ProxyCheckerMixin:

    def __init__(self) -> None:
        self.check_proxies: _Callable = check_proxies
        self.check: _Callable = check


class ProxyParserMixin:

    def __init__(self) -> None:
        self.parse_proxies: _Callable = parse_proxies
        self.parse: _Callable = parse


class Proxy(ProxyCheckerMixin, ProxyParserMixin):

    def __init__(self) -> None:
        super().__init__()


class Request:

    def __init__(self) -> None:
        self.proxy = Proxy()


# $PROJECT_DIR/parsers/request/proxy/__init__.py
if __name__ == '__main__':
    from inspect import signature as _signature
    from types import FunctionType as _FunctionType

    print('[!] This module contains:\n')
    for obj in locals().copy().values():
        # if item is a project function
        if isinstance(obj, _FunctionType) and obj != _signature:
            func_signature = f'def {obj.__name__}{_signature(obj)}:\n'
            func_docstring = f'\t"""{obj.__doc__}"""\n'
            print(func_signature, func_docstring)
        # if item is a project class
        elif isinstance(obj, type) and obj.__name__ != 'function':
            print(f'class {obj.__name__}:\n\t"""{obj.__doc__}"""\n')

    print('[*] Shortcuts:')
    for func in exec, print:
        func('ch = check; chp = check_proxies; p = parse; pp = parse_proxies')  # type: ignore [operator]
