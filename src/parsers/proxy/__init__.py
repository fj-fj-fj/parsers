#!/usr/bin/env python
"""Package 'request' that contais proxy parsers and checkers."""
# Parsing proxy examples:
# 1) Proxy().parse()
# 2) Request().proxy.parse()
# 3) parse()
# 4) p()

while True:
    try:
        from request.proxy_checker import check
        from request.proxy_checker import check_proxies
        from request.proxy_parser import parse
        from request.proxy_parser import parse_proxies
        from request.interfaces import AbstractProxy
        from request.interfaces import AbstractRequest
        break
    except ModuleNotFoundError:
        __import__('_patch').update_syspath(__file__)


class ProxyCheckerMixin:

    def __init__(self) -> None:
        self.check_proxies = check_proxies
        self.check = check


class ProxyParserMixin:

    def __init__(self) -> None:
        self.parse_proxies = parse_proxies
        self.parse = parse


class Proxy(AbstractProxy, ProxyCheckerMixin, ProxyParserMixin):

    def __init__(self) -> None:
        super().__init__()


class Request(AbstractRequest):

    def __init__(self) -> None:
        self.proxy = Proxy()


# $PROJECT_DIR/src/request/__init__.py
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
            print(f'class {obj.__name__}')

    print('[*] Shortcuts:')
    for func in exec, print:
        func('ch = check; chp = check_proxies; p = parse; pp = parse_proxies')  # type: ignore [operator]
