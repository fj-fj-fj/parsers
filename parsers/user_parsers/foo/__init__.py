#!/usr/bin/env python
"""
Modules:
- config
    'parsers.user_parsers.foo.config' from './foo/config.py'
- constatns
    parsers.user_parsers.foo.constants' from './foo/constats.py'
- parser (alias core)
    parsers.user_parsers.foo.parser' from './foo/parser.py'

Functions:
- main
    'parsers.user_parsers.foo.parser.main' function from './foo/parser.py'
- shortcuts
    'parsers.imports.shortcuts.<locals>._shortcuts'
- note
    lambda (simple dict-like container)
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
- ./notes.json
    File that will contain your notes (keys:values)
    Will be generated after REPR exiting

"""
from parsers.imports import importcore as _importcore
core = _importcore('foo')

from .parser import info
from .parser import main
from .parser import parser
from .parser import samples

import atexit as _atexit
from parsers.storage.files import exit_handler as _exit_handler

_atexit.register(
    _exit_handler,
    notes := lambda: vars(notes),
    file=core.constloc.SAMPLE_FILE.replace('samples', 'notes'),
    mode='a',
)

from parsers.imports import shortcuts

shortcuts = shortcuts(fn=main, nb=notes, pa=parser, ss=samples)

