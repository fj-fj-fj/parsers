# Keep __all__ in semantic order within each category.
__all__ = (
    # Program exit code
    'EXIT_CODE',
    # Content types
    'HTML',
    'Json',
    'Content',
    'HashableSequence',
    'KeypathStr',
    'KeyAttrValue',
    # Content handlers
    'AttrPathHandler',
    'KeyPathHandler',
    'KeyAttrFinder',
    'MakeSoupCallable',
    'ResponseLike',
    'fetch_values_by_keys',
    # Files
    'OpenMode',
    # Samples
    'SampleStr',
    'SampleList',
    'OptionalSampleList',
    'Sample',
    # Decorators
    'classproperty',
    # Metaclasses
    'NoSetter',
    # other
    'is_instance',
)

import typing as _t
from enum import StrEnum as _StrEnum
from dataclasses import dataclass as _dataclass

from bs4 import BeautifulSoup as _BeautifulSoup

from parsers.exceptions import EmptyError

EXIT_CODE: _t.Final = int

HTML: _t.TypeAlias = str
_Json: _t.TypeAlias = object | str | int | float | bool | None
Json: _t.TypeAlias = dict[str, _Json] | list[_Json]


class NoSetter(type):

    __setattr__ = lambda *_: None  # noqa: E731


@_t.final
class Content(metaclass=NoSetter):
    """Content type container"""
    HTML: _t.TypeAlias = HTML
    JSON: _t.TypeAlias = Json
    UNION_HTML_JSON: _t.TypeAlias = HTML | Json
    UNION_HTML_SOUP_JSON: _t.TypeAlias = HTML | _BeautifulSoup | Json
    UNION_SOUP_JSON: _t.TypeAlias = _BeautifulSoup | Json

    __setattr__ = NoSetter.__setattr__


class MakeSoupCallable(_t.Protocol):

    def __call__(self, *args: tuple[HTML, str | None]) -> _BeautifulSoup:
        ...


class classproperty(property):
    """Property class method"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


@_t.final
class OpenMode(_StrEnum):
    APPEND: _t.Final = 'a'
    BINARY: _t.Final = 'b'
    READ: _t.Final = 'r'
    WRITE: _t.Final = 'w'


SampleStr: _t.TypeAlias = str
SampleList: _t.TypeAlias = list[SampleStr]
OptionalSampleList: _t.TypeAlias = list[SampleStr | None] | None


class Sample(list):
    """Container to hodl parsing samples"""

    def __init__(self, *args: OptionalSampleList, file: str):
        """Init Sample object and touch `file`"""
        super().__init__(*args)
        open(file, 'a').close()
        self.file = file

    def save(self, mode=OpenMode.WRITE, truncate: bool = False) -> int:
        """Save samples or clear `self.file` if `truncate`"""
        with open(self.file, mode) as fh:
            if truncate:
                return 0
            return fh.writelines(f'{line}\n' for line in self)

    def read(self, mode=OpenMode.READ) -> SampleList:
        with open(self.file, mode) as fh:
            return [line.strip() for line in fh.readlines()]

    # GOTO: __add__ (validate key_)

    @_t.final
    @property
    def wc(self) -> str:
        """Print newline, and byte counts for `self.file`"""
        with open(self.file) as fh:
            readed = fh.read()
            chars, lines = len(readed), readed.count('\n')
            return f'{chars=} {lines=}'


class ResponseLike(_t.Protocol):
    """Ojbect with `text` property and `json` method"""

    def json(self) -> Json:
        ...

    @property
    def text(self) -> str:
        ...


def is_instance(obj, *supers, but_not=...):
    return (False, True)[isinstance(obj, *supers) and not isinstance(obj, but_not)]


class KeypathStr(str):
    """String as 'A<separator>B<separator>C'"""

    def __init__(self, keypath: str, sep='.'):
        assert sep in keypath, (keypath, sep)
        super().__init__()


@_dataclass
class KeyAttrValue:
    key_value: list | None
    attr_value: list | None


class _JsonArrayAsDict(_t.TypedDict, total=False):
    data: list[_Json]


HashableSequence: _t.TypeAlias = str | _t.Sequence[str]


class KeyPathHandler(dict):
    """Return last key value or None.

    >>> data = {"foo": {"bar": {"baz": ['egg', 'spam', 'lol']}}}
    >>> KeyPathHandler(data).get('foo.bar.baz')
    ['egg', 'spam', 'lol']

    >>> data = {"foo": {"bar": 666}}
    >>> KeyPathHandler(data).get(keypath='foo bar', sep=' ')
    [666]

    >>> KeyPathHandler().get("spam")
    >>> # None

    >>> data = {"foo": {"bar": {"x": 666}}}
    >>> KeyPathHandler(data).get('x')
    >>> # None

    """
    def get(self, keypath: HashableSequence, default=None, *, sep='.') -> list | None:
        if not self:
            return default
        if isinstance(keypath, (str, KeypathStr)):
            keypath = keypath.split(sep)

        dict_copy = self.copy()
        for key in keypath:
            value = dict_copy.get(key, default)
            if value is None:
                return default
            if isinstance(value, _t.Sequence):
                return list(value) or default
            elif isinstance(value, dict):
                dict_copy = value
            else:
                return [value]
        return default


class AttrPathHandler:
    """
    >>> AttrPathHandler().get(keys='foo.get', obj=AttrPathHandler)
    [<function AttrPathHandler.get at 0x...>]
    >>> >>> AttrPathHandler().get(keys='json', obj=AttrPathHandler)
    >>> # None

    """
    def get(self, keypath: HashableSequence, *, obj: object, sep='.') -> list | None:
        if isinstance(keypath, (str, KeypathStr)):
            keypath = keypath.split(sep)
        return [
            getattr(obj, attr) for attr in keypath
            if hasattr(obj, attr)
        ] or None


class KeyAttrFinder:
    """Value finder in `data` and `obj` by `keypath`.

    >>> data = {"foo": {"bar": ['egg', 'spam',]}}
    >>> KeyAttrFinder(data=data, obj=...)('foo.bar')
    KeyAttrValue(key_value=None, attr_value=None)

    >>> KeyAttrFinder(data=data, obj=...)('nonne')
    KeyAttrValue(key_value=['egg', 'spam'], attr_value=None)

    """
    def __init__(self, *, data: Json = None, obj: object = None, sep='.'):
        data = self.ensure_consistent_type(data)

        # To map value by keypath(s)
        self.keypath_handler = KeyPathHandler(data)
        # To map value by attribute(s)
        self.attrpath_handler = AttrPathHandler()

        self.data = data
        self.obj = obj
        # keypath separator for: a.b.c -> [a, b, c]
        self.sep = sep

    def __call__(self, keypath, *, sep=None) -> KeyAttrValue:
        assert self.obj is not None, self.__dict__

        if isinstance(keypath, (str, KeypathStr)):
            keypath = keypath.split(sep or self.sep)

        return KeyAttrValue(
            self.keypath_handler.get(keypath, sep=sep or self.sep),
            self.attrpath_handler.get(keypath, obj=self.obj, sep=sep or self.sep)
        )

    @staticmethod
    def ensure_consistent_type(maybe_dict) -> dict | _JsonArrayAsDict:
        """Return `maybe_dict` or {'data': `maybe_dict`}"""
        return maybe_dict if isinstance(maybe_dict, dict) else {'data': maybe_dict}


def fetch_values_by_keys(*, data: Json, obj: object, keypath: HashableSequence) -> KeyAttrValue:
    """Return values from `data` and `obj` by `keypath`.

    >>> data={"foo": {"bar": {"get": ['egg']}}}

    >>> fetch_values_by_keys(data=data, keypath='boo.bar.get', obj=dict)
    KeyAttrValue(key_value=['egg'], attr_value=[<method 'get' of 'dict' objects>])

    >>> fetch_values_by_keys(data=data, keypath=['sick'], obj=...)
    KeyAttrValue(key_value=None, attr_value=None)

    """
    return KeyAttrFinder(data=data, obj=obj)(keypath=keypath)
