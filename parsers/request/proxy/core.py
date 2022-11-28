#!/usr/bin/env python
"""Package 'proxy' that contais proxy parsers and checkers."""

from typing import Callable

if is_script := __name__ == '__main__':
    __import__('_patch').update_syspath(__file__)

from parsers.interfaces import AbstractProxy
from parsers.interfaces import AbstractRequest
from parsers.request.proxy.checker import check
from parsers.request.proxy.checker import check_proxies
from parsers.request.proxy.parser import parse
from parsers.request.proxy.parser import parse_proxies


class ProxyCheckerMixin:

    def __init__(self) -> None:
        self.check_proxies: Callable = check_proxies
        self.check: Callable = check


class ProxyParserMixin:

    def __init__(self) -> None:
        self.parse_proxies: Callable = parse_proxies
        self.parse: Callable = parse


class Proxy(AbstractProxy, ProxyCheckerMixin, ProxyParserMixin):

    def __init__(self) -> None:
        super().__init__()


class Request(AbstractRequest):

    def __init__(self) -> None:
        self.proxy = Proxy()


# $PROJECT_DIR/src/parsers/proxy/__init__.py
if __name__ == '__main__':
    from inspect import signature
    from types import FunctionType

    print('[!] This module contains:\n')
    for obj in locals().copy().values():
        # if item is a project function
        if isinstance(obj, FunctionType) and obj != signature:
            func_signature = f'def {obj.__name__}{signature(obj)}:\n'
            func_docstring = f'\t"""{obj.__doc__}"""\n'
            print(func_signature, func_docstring)
        # if item is a project class
        elif isinstance(obj, type) and obj.__name__ != 'function':
            print(f'class {obj.__name__}:\n\t"""{obj.__doc__}"""\n')

    print('[*] Shortcuts:')
    for func in exec, print:
        func('ch = check; chp = check_proxies; p = parse; pp = parse_proxies')  # type: ignore [operator]
