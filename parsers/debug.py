#!/usr/bin/env python
__all__ = (
    'Debug',
    'debugcls',
    'methods_and_properties',
)

import functools as _functools
import os as _os
import sys as _sys
import time as _time
import types as _types
import typing as _t

import bs4 as _bs4


class _DebugCache:
    cache: list[dict[str, _t.Any]] = []


class Debug:

    def __init__(self, method_or_property, stream=_sys.stderr):
        self.print(f'Debug.__init__(), {method_or_property=}')
        _functools.update_wrapper(self, method_or_property)
        self.m_or_p = method_or_property
        self.stream = stream

    def __call__(self, *args, **kwargs):
        self.print(f'Debug.__call__(), {args=}, {kwargs=}')
        return self.handle(*args, **kwargs)

    def __get__(self, instance, cls):
        self.print(f'Debug.__get__() {instance=}, {cls=}')
        return _types.MethodType(self, instance or cls)

    def handle(self, *args, **kwargs):
        self.print(f'Debug.handle(), {args=}, {kwargs=}')
        self.print_function_signature(*args, **kwargs)
        value = self.print_runtime(*args, **kwargs)
        _DebugCache.cache.append({self.m_or_p: value})
        self.print(f'  {_DebugCache.cache=}')
        if isinstance(value, (str, _bs4.BeautifulSoup)):
            print('  bs4 value')
            return value[:40]
        return value

    def print_function_signature(self, *args, **kwargs):
        self.print(f'Debug.print_function_signarure(), {args=}, {kwargs=}')
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        print(f" Calling {self.fname_color()}({signature})\n", file=self.stream)

    def fname_color(self):
        return f'\033[0;36m{self.m_or_p.__qualname__}\033[0m'

    def print_runtime(self, *args, **kwargs):
        self.print(f'Debug.print_runtime(), {args=}, {kwargs=}')
        start_time = _time.perf_counter()
        value = self.m_or_p(*args, **kwargs)
        run_time = _time.perf_counter() - start_time
        print(f" Finished '{self.fname_color()}' in {run_time:.5f} secs", file=self.stream)
        print(f"  '{self.fname_color()}' returned {value!r}\n", file=self.stream)
        return value

    def print(self, *args, **kwargs):
        print(*args, **kwargs) if _os.getenv('DEBUG') == '11' else None


def methods_and_properties(wrapped=None, *, worker):
    if wrapped is None:
        return _functools.partial(methods_and_properties, worker=worker)

    def inner():
        for attr in (cls := wrapped()).__dict__:
            cls_attr = getattr(cls, attr)
            if (callable(cls_attr) or 'property' in str(cls_attr)):
                setattr(cls, attr, worker(getattr(cls, attr)))
        return cls
    return inner


def debugcls(cls=None, *, manager=methods_and_properties, worker=Debug):
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
            print('response called')

        def parse(self):
            return self.parsed

        @property
        def parsed(self):
            print('parsed called')

        def save(self):
            return self.saved

        @property
        def saved(self):
            print('saved called')

    f = Foo()
    f.request()
    f.parse()
    f.save()
