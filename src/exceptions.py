#!/usr/bin/env python
"""Package 'exceptions' that contains errors and warnings."""

__all__ = 'ElementNotFoundError', 'info', 'raise_notfound'


class BaseExceptionShell(Exception):
    """Base shell for all exceptions."""


class ElementNotFoundError(BaseExceptionShell):
    """Parsed object has no element."""


def raise_notfound(tag: str):
    """Raise <tag>NotFoundError."""
    raise _notfound_factory(tag)


def _notfound_factory(prefix, bases=(ElementNotFoundError,)) -> ElementNotFoundError:
    """Return created <prefix>NotFoundError."""
    class NotFoundCreator:

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

    return NotFoundCreator().create(prefix)


def info():
    """Display imformation about this module and exceptions."""
    print(__doc__, _get_exception_classes_info(), sep='\n')


def _get_exception_classes_info(_names=('__main__', 'exceptions')) -> str:
    output = '\nexception classes:\n'
    output += '-' * len(output)
    for name, obj in globals().copy().items():
        if isinstance(obj, type) and obj.__module__ in _names:
            output += f'\n{name}:\n'
            output += f"\t'''{obj.__doc__}'''\n"
            output += f'\tmro={[o.__name__ for o in obj.mro()]}'
    return output


if __name__ == '__main__':
    info()
