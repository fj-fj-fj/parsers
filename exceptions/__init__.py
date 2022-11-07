"""This package contains errors and warnings"""

from typing import Type as _Type
from typing import TypeVar as _TypeVar


class BaseExceptionShell(Exception):
    """Base shell for all exceptions"""


class BaseRequestException(BaseExceptionShell):
    """Base shell for all requesting exceptions"""


class BaseParserException(BaseExceptionShell):
    """Base shell for all parsing exceptions"""


class ElementNotFoundException(BaseParserException):
    """Base shell for not-found-tags"""


_Self = _TypeVar('_Self', bound='NotFoundCreator')


class NotFoundCreator:

    @classmethod
    def create(cls: _Type[_Self], exception_name: str):
        """Create/return <exception_name>NotFoundError"""
        return cls._create_new_exception(f'{exception_name.capitalize()}NotFoundError')

    @staticmethod
    def _create_new_exception(
        name,
        superclasses=(ElementNotFoundException,),
        **attributedict,
    ) -> type:
        """Use type() to create exception with default base"""
        return type(name, superclasses, attributedict)


def raise_notfound(tag: str):
    """Raise <tag>NotFoundError"""
    raise notfound_factory(exception_name=tag)


def notfound_factory(exception_name) -> ElementNotFoundException:
    """Create/return <exception_name>NotFoundError using NotFoundCreator"""
    return NotFoundCreator().create(exception_name)


def print_exceptions_mro(_names=('__main__', 'exceptions')):
    """Print exeptions of this package (as class name: mro=[...])"""
    output = "\n'exceptions' package contains:\n"
    output += '-' * len(output)
    for name, obj in globals().copy().items():
        if isinstance(obj, type) and obj.__module__ in _names:
            output += f'\n{name}:\n\tmro={[o.__name__ for o in obj.mro()]}'
    print(output)


if __name__ == '__main__':
    print(print_exceptions_mro())
