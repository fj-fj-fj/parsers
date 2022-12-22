# mypy: disable-error-code=attr-defined
import glob as _glob
from io import TextIOWrapper as _TextIOWrapper
import json as _json
import os as _os
from types import LambdaType as _LambdaType
from typing import no_type_check as _no_type_check

from parsers.datatypes import Json as _Json
from parsers.interfaces import DataStorage as _DataStorage


def exit_handler(func: _LambdaType, file='./notes.json', mode='w') -> None:
    """Save `func` attributes to `file` with `mode`.

    `exit_handler` must be registered to be executed as termination.
    """
    data = str(func()).replace("'", '"')
    with open(file, mode) as notes, open(_os.devnull, 'w') as devnull:
        print(data, file=notes if eval(data) else devnull)


def save_to_file(data: str, file: str, log=True, mode='w') -> None:
    if log: print(f'saving data to {file}...')  # noqa: E701
    _os.makedirs(_os.path.dirname(file), exist_ok=True)
    with open(file, mode) as f:
        f.write(data)
    if log: print('- saved successfully!')  # noqa: E701


class File:

    @_no_type_check  # setter make data as str always
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
    def check(cls, __parsed_dir: str):
        print(f'Checking {__parsed_dir}...')
        try:
            file = _os.listdir(__parsed_dir)[0]
            with open(file) as fh:
                return File(fh.read())
        except (FileNotFoundError, IndexError):
            return

    def json(self) -> _Json:
        """Return _Json or raise json.decoder.JSONDecodeError"""
        assert isinstance(self.data, str)
        return _json.loads(self.data)

    @property
    def text(self) -> str:
        return self.data


class _FileCheckerMixin:
    """Mixin to add count,create files functionality"""

    def __init__(self):
        self.number_of_files = self._count_files
        self.file = f'{self.parsed_dir}/{self.STEM}{self._suffix}'

    def create_file_if_not_exists(self) -> None:
        if _os.path.exists(self.file):
            last_file = self._files[-1]
            n = _os.path.basename(last_file)[0]
            n_plus_one = str(self._count_files + 1)
            self.file = last_file.replace(n, n_plus_one)
        _os.makedirs(self.parsed_dir, exist_ok=True)

    @property
    def _count_files(self) -> int:
        """(property) Return count of *.(specific ext)"""
        self._files = _glob.glob(f'{self.parsed_dir}/*{self._suffix}')
        return len(self._files)

    @property
    def _suffix(self) -> str:
        """(property) Return mapped ext"""
        return {
            'JsonStorage': '.json',
            'PlainStorage': '.html',
        }[self.__class__.__name__]


class PlainStorage(_DataStorage, _FileCheckerMixin):
    """Store data in plain text file"""

    def __init__(self, parsed_dir: str = None):
        self.parsed_dir = parsed_dir or self.PARSED_DIR
        super().__init__()

    def save(self, data: str, mode: str = 'w') -> int:  # type: ignore
        self.data = data
        self.create_file_if_not_exists()
        with open(self.file, mode) as fh:
            return fh.write(data)


class JsonStorage(_DataStorage, _FileCheckerMixin):
    """Store data in json file"""

    def __init__(self, parsed_dir: str = None):
        self.parsed_dir = parsed_dir or self.PARSED_DIR
        super().__init__()

    def save(self, data: _Json, mode: str = 'w') -> int:
        self.data = data
        self.create_file_if_not_exists()
        with open(self.file, mode) as fh:
            return fh.write(_json.dumps(data))


Storage = PlainStorage | JsonStorage


class ContextStorage:
    """Manager to map stored data with `DataStorage` subclasses"""

    def __init__(self):
        self.current = None

    def map(self, keytype: str) -> 'ContextStorage':
        self.current = {
            'str': PlainStorage,
            'list': JsonStorage,
            'dict': JsonStorage,
        }[keytype]

        return self


def pyclean() -> None:
    import pathlib
    for p in pathlib.Path('.').rglob('*.py[co]'):
        p.unlink()
    for p in pathlib.Path('.').rglob('__pycache__'):
        p.rmdir()
