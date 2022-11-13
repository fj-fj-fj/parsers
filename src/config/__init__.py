
from dataclasses import dataclass


@dataclass
class Configuration:
    """Contains keys: url, file_parsed, file_response, parser"""
    url: str = None
    file_parsed: str = None
    file_response: str = None
    parser: str = None

    def __post_init__(self):
        self.__KeyStorage = type('__KeyStorage', (), {})
        for key in self.__dict__:
            if key:
                setattr(self.__KeyStorage, key, key)

    def setdefault(self, key: str, value: str):
        if getattr(self, key) is None:
            setattr(self, key, value)

    @property
    def key(self):
        return self.__KeyStorage
