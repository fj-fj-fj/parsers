from os import makedirs as _makedirs
from os.path import dirname as _dirname
from typing import Type as _Type

from requests import Response as _Response

from parsers.datatypes import StrOrJson as _StrOrJson
from parsers.interfaces import DataStorage as _DataStorage


def save_to_file(data: str, file: str, log=True, mode='w') -> None:
    if log: print(f'saving data to {file}...')  # noqa: E701
    _makedirs(_dirname(file), exist_ok=True)
    with open(file, mode) as f:
        f.write(data)
    if log: print('- saved successfully!')  # noqa: E701


class PlainStorage(_DataStorage):
    """Store data in plain text file"""

    _RAW_DATA_FILE = 'response.html'

    def __init__(self, data, parsed_dir: str = None) -> None:
        self.file = (parsed_dir or self.PARSED_DIR) + PlainStorage._RAW_DATA_FILE
        self.data = data

    def save(self, data, mode: str = 'w') -> None:
        _makedirs(_dirname(self.file), exist_ok=True)
        with open(self.file, mode) as f:
            f.write(data)


class JsonStorage(_DataStorage):
    """Store data in json file"""

    _RAW_DATA_FILE = 'response.json'

    def __init__(self, data, parsed_dir: str = None) -> None:
        self.file = (parsed_dir or self.PARSED_DIR) + JsonStorage._RAW_DATA_FILE
        self.data = data

        self._utils = __import__('json')

    def save(self, data, mode: str = 'w') -> None:
        self.data = data or self.data
        _makedirs(_dirname(self.file), exist_ok=True)
        with open(self.file, mode) as f:
            f.write(self._utils.dumps(data))


class ContextStorage:
    """Manager to map stored data with `DataStorage` subclasses"""

    def __init__(self, data: _Response = None, dirname: str = None) -> None:
        self._data = data
        self._dirname = dirname

    def map(self, keytype: _Type[_StrOrJson]) -> _Type[_DataStorage]:
        return {_Type[str]: PlainStorage, _Type[list]: JsonStorage}[_Type[keytype]]

    def update(self, data: _Response, dirname: str) -> None:
        self._data = data
        self._dirname = dirname

    def update_ifnot_exist(self, data: _Response, dirname: str) -> None:
        self._data = self._data or data
        self._dirname = self._dirname or dirname
