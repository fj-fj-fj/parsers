#!/usr/bin/env python
__all__ = (
    'Debug',
    'debugcls',
    'methods',
    'functions',
)
import functools as _functools
import os as _os
import sys as _sys
import time as _time
import types as _types
import typing as _t
from textwrap import dedent as _dedent

import bs4 as _bs4

if is_script := __name__ == '__main__':
    (lambda d: _sys.path.insert(0, d(d(__file__))))(_os.path.dirname)

from parsers.constants import Constant as _Constant
from parsers.datatypes import OpenMode as _OpenMode
from parsers.format.colors import Colors as _Colors
from parsers.format.colors import remove_escape_sequences as _remove_escape_sequences
from parsers.storage.files import TeeFile as _TeeFile

FuncNameColorBlueStr: _t.TypeAlias = str
ValueColorYellowStr: _t.TypeAlias = str

# Redirect out to console and to 'log/debug.err'
_sys.stderr = _TeeFile(  # type: ignore
    _sys.__stderr__,
    open(_Constant.FILE.DEBUG_ERR, _OpenMode.WRITE),
    # write output without '\x1B[...' and first space
    optional_handler=lambda s: _remove_escape_sequences(s.lstrip())
)


class Debug:
    """Debug() is an inner decorator (for args, kwargs)"""

    def __init__(self, method_or_property, verbose, stream=_sys.stderr):
        self._print_debug_11(f'Debug.__init__({method_or_property=}, {verbose=}, {stream=})')
        self._m_or_p = method_or_property
        self.verbose = verbose
        self.stream = stream
        self.cache = []
        self._ = None

    def __call__(self, *args, **kwargs):
        self._print_debug_11(f'Debug.__call__({args=}, {kwargs=})')
        return self.handle(*args, **kwargs)

    def __get__(self, instance, cls):
        self._print_debug_11(f'Debug.__get__({instance=}, {cls=})')
        return _types.MethodType(self, instance or cls)

    def handle(self, *args, **kwargs):
        """Main debug handler"""
        self._print_debug_11(f'Debug.handle({args=}, {kwargs=})')

        self._print_function_signature(*args, **kwargs)
        self._print_runtime(*args, **kwargs)
        self._print_result_wrapped(*args, **kwargs)

        self.cache.append({self._m_or_p: self._})
        self._print_debug_11(f'  {self.cache=}')
        return self._

    def _print_function_signature(self, *args, **kwargs) -> None:
        self._print_debug_11(f'Debug._print_function_signature({args=}, {kwargs=})')
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        # $ Calling 'Foo.bar(<__main__.Foo object at 0x...>)'
        print(f" Calling '{self.colorize_fname()}({signature})'\n", file=self.stream)

    def _print_runtime(self, *args, **kwargs) -> None:
        self._print_debug_11(f'Debug._print_runtime({args=}, {kwargs=})')

        start_time = _time.perf_counter()
        self.excecute_wrapped(*args, **kwargs)
        elapsed = _time.perf_counter() - start_time

        # $ Finished 'Foo.bar' in <float> secs
        print(f" Finished '{self.colorize_fname()}' in {elapsed:.5f} secs", file=self.stream)

    def _print_result_wrapped(self, *args, **kwargs) -> None:
        self._print_debug_11(f'Debug._print_result_wrapped({args=}, {kwargs=})')

        co_names = self._m_or_p.__code__.co_names
        # $  'Foo.bar' works with ('baz', ...)
        print(f"  '{self.colorize_fname()}' works with {co_names}", file=self.stream)

        result = self.colorize_value(self._)
        # $    'Foo.bar' returned 'bla bla' (if not self.verbose)
        # $    'Foo.bar' returned 'baz' with result='bla bla'
        print('  ', _dedent(f"""\
            '{self.colorize_fname()}' returned {
                f"'{self.colorize_fname(co_names[-1])}' with result='{result}'"
                if self.verbose
                else result
            }\n
            """),
            file=self.stream)  # noqa: E128

    def excecute_wrapped(self, *args, **kwargs) -> None:
        self._ = self._m_or_p(*args, **kwargs)
        # less output
        if isinstance(self._, _bs4.BeautifulSoup):
            self._ = 'BeautifulSoup content here [...]'
        elif isinstance(self._, str) and "<!DOCTYPE" in self._:
            self._ = 'HTML content here [...]'

    def colorize_fname(self, name=None) -> FuncNameColorBlueStr:
        return f'{_Colors.BLUE}{name or self._m_or_p.__qualname__}{_Colors.NC}'

    def colorize_value(self, __v) -> ValueColorYellowStr:
        return f'{_Colors.YELLOW}{__v}{_Colors.NC}'

    def _print_debug_11(self, *args, **kwargs) -> None:
        """Selfdebug. Display args, kwargs if DEBUG=11"""
        if _os.getenv('DEBUG') == '11':
            print(*args, **kwargs)


def functions(wrapped=None, *, worker):
    return NotImplemented


def methods(wrapped=None, *, worker, verbose):
    if wrapped is None:
        return _functools.partial(methods, worker=worker, verbose=verbose)

    def inner(*args, **kwargs):
        cls = wrapped()
        _functools.update_wrapper(inner, cls)
        for attr in cls.__dict__:
            cls_attr = getattr(cls, attr)
            if callable(cls_attr):
                setattr(cls, attr, worker(cls_attr, verbose=verbose))
        return cls(*args, **kwargs)
    return inner


def debugcls(cls=None, *, manager=methods, worker=Debug, verbose=True):
    if cls is None:
        return _functools.partial(debugcls, manager=manager, worker=worker, verbose=verbose)
    if not _os.getenv('DEBUG', True):
        return cls
    return manager(lambda: cls, worker=worker, verbose=verbose)


if is_script:
    # @methods(worker=Debug, verbose=True)  # fail

    # @debugcls(manager=methods, worker=Debug, verbose=False)  # OK
    # @debugcls(manager=methods, worker=Debug)  # OK
    # @debugcls(verbose=False)  # OK
    # @debugcls(manager=methods)  # OK
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
    # f.response
    f.parse()
    # f.parsed
    f.save()
    # f.saved
