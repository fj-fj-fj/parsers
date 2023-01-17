#!/usr/bin/env python
__all__ = (
    'Debug',
    'debugcls',
    'methods',
    'methods_and_properties',
    'properties',
)

import functools as _functools
import os as _os
import sys as _sys
import time as _time
import types as _types

import bs4 as _bs4

from parsers.constants import Constant as _Constant
from parsers.datatypes import OpenMode as _OpenMode
from parsers.format.colors import Colors as _Colors
from parsers.format.colors import remove_escape_sequences as _remove_escape_sequences
from parsers.storage.files import TeeFile as _TeeFile

# Redirect out to console and to 'log/debug.err'
_sys.stderr = _TeeFile(  # type: ignore
    _sys.__stderr__,
    open(_Constant.FILE.DEBUG_ERR, _OpenMode.WRITE),
    # write output without '\x1B[...' and first space
    optional_handler=lambda s: _remove_escape_sequences(s.lstrip())
)


class Debug:

    def __init__(self, method_or_property, stream=_sys.stderr):
        self._s_init__ = f'Debug.__init__(), {method_or_property=}'
        self._print(self._s_init__)
        self._m_or_p = method_or_property
        self.stream = stream
        self.cache = []
        self._ = None

    def __call__(self, *args, **kwargs):
        self._s_call__ = f'Debug.__call__(), {args=}, {kwargs=}'
        self._print(self._s_call__)
        return self.handle(*args, **kwargs)

    def __get__(self, instance, cls):
        self._s_get__ = f'Debug.__get__() {instance=}, {cls=}'
        self._print(self._s_get__)
        return _types.MethodType(self, instance or cls)

    def handle(self, *args, **kwargs):
        self._print(f'Debug.handle(), {args=}, {kwargs=}')
        self._print_function_signature(*args, **kwargs)
        self._print_runtime(*args, **kwargs)
        self.cache.append({self._m_or_p: self._})
        self._print(f'  {self.cache=}')
        return self._

    def _print_function_signature(self, *args, **kwargs):
        self._print(f'Debug._print_function_signarure(), {args=}, {kwargs=}')
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        print(f" Calling '{self.colorize_fname()}({signature})'\n", file=self.stream)

    def _print_runtime(self, *args, **kwargs):
        self._print(f'Debug._print_runtime(), {args=}, {kwargs=}')
        start_time = _time.perf_counter()

        self.excecute_wrapped(*args, **kwargs)

        runtime = _time.perf_counter() - start_time
        print(f" Finished '{self.colorize_fname()}' in {runtime:.5f} secs", file=self.stream)
        print(f"  '{self.colorize_fname()}' returned {self._!r}\n", file=self.stream)

    def colorize_fname(self):
        return f'{_Colors.BLUE}{self._m_or_p.__qualname__}{_Colors.NC}'

    def _print(self, *args, **kwargs):
        if _os.getenv('DEBUG') == '11':
            print(*args, **kwargs)

    def excecute_wrapped(self, *args, **kwargs):
        self._ = self._m_or_p(*args, **kwargs)
        if isinstance(self._, _bs4.BeautifulSoup):
            self._ = 'BeautifulSoup content here [...]'
        elif isinstance(self._, str) and "<!DOCTYPE" in self._:
            self._ = 'HTML content here [...]'


def methods_and_properties(wrapped=None, *, worker):
    if wrapped is None:
        return _functools.partial(methods, worker=worker)

    def inner(*args, **kwargs):
        cls = wrapped()
        _functools.update_wrapper(inner, cls)
        for attr in cls.__dict__:
            cls_attr = getattr(cls, attr)
            if callable(cls_attr) or 'property' in str(cls_attr):
                value = worker(getattr(cls, attr))
                setattr(cls, attr, value)
        return cls(*args, **kwargs)
    return inner


def properties(wrapped=None, *, worker):
    return NotImplemented


def methods(wrapped=None, *, worker):
    if wrapped is None:
        return _functools.partial(methods, worker=worker)

    def inner(*args, **kwargs):
        cls = wrapped()
        _functools.update_wrapper(inner, cls)
        for attr in cls.__dict__:
            cls_attr = getattr(cls, attr)
            if callable(cls_attr):
                setattr(cls, attr, worker(cls_attr))
        return cls(*args, **kwargs)
    return inner


def debugcls(cls=None, *, manager=methods, worker=Debug):
    if cls is None:
        return _functools.partial(debugcls, manager=manager, worker=worker)
    if not _os.getenv('DEBUG', True):
        return cls
    return manager(lambda: cls, worker=worker)


if __name__ == '__main__':
    # @methods_and_properties  # fail
    # @methods_and_properties(worker=Debug)  # fail
    # @debugcls(manager=methods_and_properties, worker=Debug)  # OK
    @debugcls  # OK
    class Foo:
        def request(self):
            return self.response

        @property
        def response(self):
            return 'response called'

        def parse(self):
            return self.parsed

        @property
        def parsed(self):
            return 'parsed called'

        def save(self):
            return self.saved

        @property
        def saved(self):
            return 'saved called'

    f = Foo()
    f.request()
    f.parse()
    f.save()
