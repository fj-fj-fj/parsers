"""exit handlers"""
__all__ = [
    'register_exit_func',
    'save_notes',
]
import os as _os
import atexit as _atexit
import signal as _signal
import sys as _sys
import typing as _t
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)


_HANDLER: _t.TypeAlias = _t.Callable


@_dataclass
class _ExitFuncState:
    registered: set[_HANDLER] = _field(default_factory=set)
    executed: set[_HANDLER] = _field(default_factory=set)


_EXIT_FUNCS = _ExitFuncState()

_EXIT_SIGNALS = frozenset([
    _signal.SIGTERM,
    _signal.SIGINT,
    _signal.SIGQUIT,
    _signal.SIGABRT,
    # _signal.SIGHUP,
])


def register_exit_func(__func: _HANDLER, *, _signals=_EXIT_SIGNALS, **kwds) -> None:  # noqa: C901
    """Register `__func` which will be executed on exit.

    Also, it makes sure to execute any previously registered
    via `_signal.signal()`. If any, it will be executed after `__func`.
    Functions which were already registered or executed will be skipped.
    Exit function will not be executed on `SIGKILL`,`SIGSTOP` or `os._exit()`.

    If os.name != 'posix' than `OSError` will be raise.

    """
    if _os.name != 'posix':
        raise OSError('POSIX only')

    def func_wrapper() -> None:
        if __func not in _EXIT_FUNCS.executed:
            try:
                __func()
            finally:
                _EXIT_FUNCS.executed.add(__func)

    def signal_wrapper(signum=None, frame=None) -> None:
        func_wrapper()

        # os.kill(os.getpid(), signal.<SIGNAL>)
        if signum is not None:
            if signum == _signal.SIGINT:
                raise KeyboardInterrupt
            _sys.exit(signum)

    if not callable(__func):
        raise TypeError(f'{__func!r} is not callable')

    for sig in _signals:
        old_handler = _signal.signal(sig, signal_wrapper)
        if old_handler not in (_signal.SIG_DFL, _signal.SIG_IGN):
            if not callable(old_handler):
                continue
            if sig == _signal.SIGINT and old_handler is _signal.default_int_handler:
                continue
            if old_handler not in _EXIT_FUNCS.registered:
                _atexit.register(old_handler, **kwds)  # type: ignore [call-arg]
                _EXIT_FUNCS.registered.add(old_handler)

    # Clean interpreter exit (no signals received)
    if __func not in _EXIT_FUNCS.registered or not _signals:
        _atexit.register(func_wrapper, **kwds)
        _EXIT_FUNCS.registered.add(__func)


def save_notes(__func, *, to='', basename='notes.txt', mode='a') -> _HANDLER:
    """Save notes before exiting the program.

    Example:
    ```
        # parsers.user_parsers.<parser>.__init__.py
        from parsers.utils.exit import register_exit_func, save_notes
        note, dir = lambda: vars(note), core.constloc.PARSED_DIR
        register_exit_func(save_notes(note, to=dir))
    ```
    Expected key args:
        `(to='path/to/', basename='name')`
        or `(to='path/to/file', basename=None)`
    else will be raise `parsers.exceptions.ParameterValueError`
    ```
    """
    file = f'{to}/{basename}' if basename else to
    while '//' in (file := file.replace('//', '/')):
        pass
    if not file:
        from parsers.exceptions import ParameterValueError
        raise ParameterValueError(f'{dir=}, {file=}\n{__doc__}')

    def inner_save_notes() -> None:
        with open(file, mode or 'a') as fh, open(_os.devnull, 'w') as devnull:
            print(
                valid_json_data := str(__func()).replace("'", '"'),
                file=fh if valid_json_data != r'{}' else devnull
            )
    return inner_save_notes
