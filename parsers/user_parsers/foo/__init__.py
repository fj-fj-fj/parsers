#!/usr/bin/env python
# mypy: ignore-errors
"""
Modules:
- logic
    'parsers.user_parsers.foo.logic' from './foo/logic.py'
- constatns
    'parsers.user_parsers.foo.constants' from './foo/constats.py'
- parser (alias core)
    'parsers.user_parsers.foo.parser' from './foo/parser.py'

Functions:
- main
    'parsers.user_parsers.foo.parser.main' function from './foo/parser.py'
- shortcuts
    'parsers.imports.shortcuts.<locals>._shortcuts'
- note
    (lambda) Simple dict-like container
    Use ad-hoc attributes to hodl smth
    Will be automatically saved to ./notes.json

Classes:
- info
    'parsers.imports.ModuleDocstring' instance from './foo/parser.py'
- parser
    'parsers.handlers.Parser' instance from './foo/parser.py'
- samples
    'parsers.datatypes.Sample' list-like instance from './foo/parser.py'

Files:
- ./samples.txt
    File that will contain your samples (strings)
    Will be generated after `samples.save()`
- ./notes.txt
    File that will contain your notes (keys:values)
    Will be generated after REPL exiting

"""
from parsers.imports import importcore as _importcore
core = _importcore('foo')

from .parser import info
from .parser import main
from .parser import parser
from .parser import samples


note = lambda: vars(note)  # noqa: E731


from parsers.imports import shortcuts
shortcuts = shortcuts(fn=main, nb=note, pa=parser, ss=samples)

from parsers.utils.exit import register_exit_func, save_notes
register_exit_func(save_notes(note, to=core.constloc.PARSED_DIR))
