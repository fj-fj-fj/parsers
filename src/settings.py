"""The 'settings' module contains Configuration() for default **kwargs."""
from dataclasses import dataclass
from typing import Type

from constants import ConstantStorage


@dataclass
class Configuration:
    """Default kwargs"""

    url: str = None
    parser: str = None
    file_parsed: str = None
    file_response: str = None

    def __post_init__(self) -> None:
        """Create container with Configuration() attribute names."""
        self.__KeyStorage = type('__KeyStorage', (), {})
        for key in self.__dict__:
            if key:
                setattr(self.__KeyStorage, key, key)

    def setdefaults(self, const: Type[ConstantStorage]) -> None:
        """Replace None with new values in attributes."""
        self.setdefault(self.key.url, const.URL.PROXY_URL)
        self.setdefault(self.key.parser, const.PARSE.PARSER)
        self.setdefault(self.key.file_parsed, const.FILE.PARSED_PROXIES)
        self.setdefault(self.key.file_response, const.FILE.PROXY_RESPONSE)

    def setdefault(self, key: str, value: str) -> None:
        """Set new value to attribute if it is None."""
        if getattr(self, key) is None:
            setattr(self, key, value)

    @property
    def key(self):
        """Return container with Configuration() attribute names.

        All attributes contain names of the same name:
            `Literal['url', 'parser', 'file_parsed', 'file_response']`

        """
        return self.__KeyStorage
