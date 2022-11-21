#!/usr/bin/env python
"""Module 'exceptions' that contains errors and warnings."""
from typing import NoReturn

__all__ = 'ElementNotFoundError', 'raise_notfound'


class BaseError(Exception):
    """Base shell for all errors."""


class ElementNotFoundError(BaseError):
    """Has no HTML element."""


class ParameterValueError(BaseError):
    """Got an unexpected argument value."""


def raise_notfound(tag: str) -> NoReturn:
    """Raise <tag>NotFoundError."""
    raise _notfound_factory(tag)


def _notfound_factory(prefix, bases=(ElementNotFoundError,)) -> ElementNotFoundError:
    """Return created <prefix>NotFoundError."""
    class NotFound:
        @classmethod
        def create(cls, exception_prefix):
            return cls._create_exception(exception_prefix)

        @staticmethod
        def _create_exception(prefix, bases=bases, **attributedict):
            msg = f"Parsed object has no tag '{prefix}'"
            fullname = f'{prefix.capitalize()}NotFoundError'
            attributedict['__init__'] = lambda self: bases[0].__init__(self, msg)
            attributedict['__repr__'] = lambda self: repr(msg)
            return type(fullname, bases, attributedict)

    return NotFound().create(prefix)


if __name__ == '__main__':
    # Display imformation about 'exceptions' module
    # names, docstrings, mro
    information = '\nexception classes:\n'
    information += '-' * len(information)
    for name, obj in globals().copy().items():
        if isinstance(obj, type):
            information += f'\n{name}:\n'
            information += f"\t'''{obj.__doc__}'''\n"
            information += f'\tmro={[o.__name__ for o in obj.mro()]}'
    print(__doc__, information, sep='\n')
