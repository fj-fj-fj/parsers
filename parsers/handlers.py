from typing import NamedTuple as _NamedTuple
from typing import Type as _Type

from requests.exceptions import JSONDecodeError as _JSONDecodeError
from requests import Response as _Response

from parsers.datatypes import StrOrJson as _StrOrJson
from parsers.datatypes import ResponseContentStr as _ResponseContentStr
from parsers.storage.files import ContextStorage as _ContextStorage
from parsers.storage.files import PlainStorage as _PlainStorage
from parsers.storage.files import Storage as _Storage


class HandledData(_NamedTuple):
    """HandledData(data, is_json, storage)"""
    data: _StrOrJson
    is_json: bool
    storage: _Storage


class ResponseHandler:

	def __init__(
		self,
		response: _Response,
		parsed_dir: str,
		auto: bool = False,
		cstorage: _ContextStorage = None,
	) -> None:
		self.__auto = auto
		self._cstorage = cstorage or _ContextStorage()
		self._parsed_dir = parsed_dir
		self._response = response

		self._dtype: _Type[_StrOrJson] = None
		self._handled: _StrOrJson = None
		self._storage: _Storage = _PlainStorage(None)

		if self.__auto:
			self.handle()

	def handle(self) -> None:
		self._dtype = self.get_data_type()
		mapped = self.map()
		self._storage = mapped(self._handled, self._parsed_dir)  # type: ignore
		if self.__auto:
			self.save()

	def map(self, dtype: _ResponseContentStr = None) -> _Storage:
		self._dtype = dtype or self._dtype
		return self._cstorage.map(self._dtype)

	def save(self, data: _StrOrJson = None) -> None:
		self._storage.save(data or self._handled)

	@property
	def data(self) -> HandledData:
		return HandledData(
			data=self._handled,
			is_json=self._dtype in (dict, list),
			storage=self._storage,
		)

	def get_data_type(self) -> _ResponseContentStr:
		return type(self._get_data_from_response())

	def _get_data_from_response(self) -> _StrOrJson:
		try:
			self._handled = self._response.json()
		except _JSONDecodeError:
			self._handled = self._response.text
		return self._handled


def handle_data(response: _Response, parsed_dir: str) -> HandledData:
	return ResponseHandler(response, parsed_dir, auto=True).data
