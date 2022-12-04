# mypy: disable-error-code=attr-defined
# FIXME: _FileCheckerMixin has no attribute "parsed_dir" "root"
import glob as _glob
import json as _json
import os as _os
import os.path as _ospath
from typing import Type as _Type

from parsers.datatypes import StrOrJson as _StrOrJson
from parsers.interfaces import DataStorage as _DataStorage


def save_to_file(data: str, file: str, log=True, mode='w') -> None:
    if log: print(f'saving data to {file}...')  # noqa: E701
    _os.makedirs(_ospath.dirname(file), exist_ok=True)
    with open(file, mode) as f:
        f.write(data)
    if log: print('- saved successfully!')  # noqa: E701


class _FileCheckerMixin:
    """Mixin to add count,create files functionality"""

    def __init__(self) -> None:
        self.number_of_files = self._count_files
        self.file = self.root + self._suffix

    def create_file_if_not_exists(self) -> None:
        if not _os.path.exists(self.file):
            _os.makedirs(self.parsed_dir, exist_ok=True)
        else:
            last_file = self._files[-1]
            n = _ospath.basename(last_file)[0]
            n_plus_one = str(self._count_files + 1)
            self.file = last_file.replace(n, n_plus_one)
            _os.makedirs(self.parsed_dir, exist_ok=True)

    @property
    def _count_files(self) -> int:
        """(property) Return count of *.(specific ext)"""
        self._files = _glob.glob(f'{self.parsed_dir}*{self._suffix}')
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

    _STEM = '1_response'

    def __init__(self, data, parsed_dir: str = None) -> None:
        self.parsed_dir = parsed_dir or self.PARSED_DIR
        self.root = self.parsed_dir + JsonStorage._STEM
        super().__init__()

        self.data = data

    def save(self, data, mode: str = 'w') -> None:
        self.data = data or self.data
        self.create_file_if_not_exists()
        with open(self.file, mode) as f:
            f.write(data)


class JsonStorage(_DataStorage, _FileCheckerMixin):
    """Store data in json file"""

    _STEM = '1_response'

    def __init__(self, data, parsed_dir: str = None) -> None:
        self.parsed_dir = parsed_dir or self.PARSED_DIR
        self.root = self.parsed_dir + JsonStorage._STEM
        super().__init__()

        self.data = data

    def save(self, data, mode: str = 'w') -> None:
        self.data = data or self.data
        self.create_file_if_not_exists()
        with open(self.file, mode) as f:
            f.write(_json.dumps(data))


Storage = PlainStorage | JsonStorage


class ContextStorage:
    """Manager to map stored data with `DataStorage` subclasses"""

    def map(self, keytype: _Type[_StrOrJson]) -> Storage:
        return {
            _Type[str]: PlainStorage,
            _Type[list]: JsonStorage,
        }[_Type[keytype]]   # type: ignore
