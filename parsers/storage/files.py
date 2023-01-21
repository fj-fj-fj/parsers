# mypy: disable-error-code=attr-defined
__all__ = (
    'File',
    'ContextStorage',
    'JsonStorage',
    'PlainStorage',
    'TeeFile',
    'exit_handler',
    'pyclean',
    'save_to_file',
)

import glob as _glob
import json as _json
import os as _os
import sys as _sys
import typing as _t
from io import TextIOWrapper as _TextIOWrapper

from parsers.datatypes import Content as _Content
from parsers.datatypes import OpenMode as _OpenMode


# return file.write(...)
_n_chars: _t.TypeAlias = int
_int_as_str: _t.TypeAlias = str


def exit_handler(func: _t.Callable, file='./notes.json', mode=_OpenMode.APPEND) -> None:
    """Save `func` return data to `file` with `mode`"""
    with open(file, mode) as fh, open(_os.devnull, _OpenMode.WRITE) as devnull:
        print(
            valid_json_data := str(func()).replace("'", '"'),
            file=fh if valid_json_data != r'{}' else devnull
        )


def save_to_file(data: str, file: str, mode=_OpenMode.WRITE) -> _n_chars:
    _os.makedirs(_os.path.dirname(file), exist_ok=True)
    with open(file, mode) as f:
        return f.write(data)


class File:

    @_t.no_type_check
    def __init__(self, data: str | _TextIOWrapper):
        self.data = data

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, _TextIOWrapper):
            with open(value) as fh:
                self._data = fh.read()
        else:
            self._data = value

    @classmethod
    def check(cls, __parsed_dir: str, truncate=False):
        try:
            file = _os.listdir(__parsed_dir)[0]
            if truncate:
                open(file, _OpenMode.WRITE).close()
            with open(file) as fh:
                return File(fh.read())
        except (FileNotFoundError, IndexError):
            return

    def json(self) -> _Content.JSON:
        """Return _Json or raise json.decoder.JSONDecodeError"""
        assert isinstance(self.data, str)
        return _json.loads(self.data)

    @property
    def text(self) -> str:
        return self.data


class _FileMixin:

    STEP_STEM_MAP = {0: '1_response', 1: '1_raw_data', 2: '1_final_data'}
    STEP_SUFFIX_MAP = {0: '.html', 1: '.tmp', 2: '.json'}
    UNKNOWN_STEM = '1_unknow_step'
    REPL_PREFIX = 'repl_'

    def define_file(self, step: int, suffix=None) -> None:
        stem = self.STEP_STEM_MAP.get(step, self.UNKNOWN_STEM)
        suffix = suffix or self.STEP_SUFFIX_MAP.get(step, '')
        basename = f'{stem}{suffix}'
        if _sys.flags.interactive:
            basename = f'{self.REPL_PREFIX}{basename}'
        self.file = f'{self.parsed_dir}/{basename}'
        _os.makedirs(self.parsed_dir, exist_ok=True)
        # GOTO: self.save(increment_prefix=False)
        # if increment_prefix: self.set_prefix_file()

    def set_prefix_file(self) -> None:
        if _os.path.exists(self.file):
            last_file = self._files[-1]
            n = _os.path.basename(last_file)[0]
            n_plus_one = self.increment(self._count_files())
            assert isinstance(n_plus_one, str)
            self.file = last_file.replace(n, n_plus_one)

    def _count_files(self) -> int:
        self._files = _glob.glob(f'{self.parsed_dir}/*{self.SUFFIX_DEFAULT}')
        return len(self._files)

    @staticmethod
    def increment(number: int, *, step=1, return_str=True) -> int | _int_as_str:
        if not isinstance(number, int):
            raise ValueError(f'{number=} must be integer.')
        if step < 1:
            raise ValueError(f'{step=} must be positive.')

        def inner_increment():
            return str(number + step) if return_str else number + step
        return inner_increment()


class PlainStorage(_FileMixin):
    """Store data in plain text file"""

    SUFFIX_DEFAULT = ''

    def __init__(self, parsed_dir: str = None):
        self.parsed_dir = parsed_dir or self.PARSED_DIR

    def save(self, data: str, *, step: int, mode=_OpenMode.WRITE, suffix=None) -> _n_chars:
        self.data = data
        self.define_file(step=step, suffix=suffix)
        with open(self.file, mode) as plain_storage_fh:
            return plain_storage_fh.write(data)

    @staticmethod
    def keys():
        return 'str', 'bs4', 'page', 'text'


class JsonStorage(_FileMixin):
    """Store data in json file"""

    SUFFIX_DEFAULT = '.json'

    def __init__(self, parsed_dir: str = None):
        self.parsed_dir = parsed_dir or self.PARSED_DIR

    def save(self, data: _Content.JSON, *, step: int, mode=_OpenMode.WRITE, suffix=None) -> _n_chars:
        self.data = data
        self.define_file(step=step, suffix=suffix)
        with open(self.file, mode) as json_storage_fh:
            return json_storage_fh.write(_json.dumps(data))

    @staticmethod
    def keys():
        return 'list', 'dict', 'json', 'obj'


_Storage = PlainStorage | JsonStorage


class ContextStorage:
    """Manager"""

    def __init__(self):
        self.current: _Storage = None
        self.sorting_hat = {
            **dict.fromkeys(PlainStorage.keys(), PlainStorage),
            **dict.fromkeys(JsonStorage.keys(), JsonStorage),
        }

    def map(self, datatype: str) -> _t.Self:  # type: ignore
        """Map <storage> by `datatype` into self.current. Return self"""
        self.current = self.sorting_hat[datatype]
        return self


def pyclean() -> None:
    """Clean Python bytecode"""
    import pathlib
    for p in pathlib.Path('.').rglob('*.py[co]'):
        p.unlink()
    for p in pathlib.Path('.').rglob('__pycache__'):
        p.rmdir()


class TeeFile:
    """Output to multiple files"""

    def __init__(
        self,
        *files: _TextIOWrapper | _t.IO[_t.Any],
        optional_handler: object = None,
        # exclude filenames from optional processing
        exclude_optional_handling='<stderr><stdout>',
    ):
        """`optional_handler`: additional text processing"""
        self.exclude = exclude_optional_handling
        self.handler = optional_handler
        self.files = files

    def write(self, text) -> _n_chars:
        def handled(text):
            if self.handler is not None and fh.name not in self.exclude:
                return self.handler(text)
        self.n_chars = 0
        for fh in self.files:
            self.n_chars += fh.write(handled(text) or text)
        return self.n_chars

    def flush(self) -> None:
        for fh in self.files:
            fh.flush()
