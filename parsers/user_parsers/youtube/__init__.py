#!/usr/bin/env python
# mypy: ignore-errors
"""
Modules:
- logic
    'parsers.user_parsers.youtube.logic' from './youtube/logic.py'
- constatns
    parsers.user_parsers.youtube.constants' from './youtube/constats.py'
- parser (alias core)
    parsers.user_parsers.youtube.parser' from './youtube/parser.py'

Functions:
- main
    'parsers.user_parsers.youtube.parser.main' function from './youtube/parser.py'
- shortcuts
    'parsers.imports.shortcuts.<locals>._shortcuts'
- note
    (lambda) Simple dict-like container
    Use ad-hoc attributes to hodl smth
    Will be automatically saved to ./notes.json

Classes:
- info
    'parsers.imports.ModuleDocstring' instance from './youtube/parser.py'
- parser
    'parsers.handlers.Parser' instance from './youtube/parser.py'
- samples
    'parsers.datatypes.Sample' list-like instance from './youtube/parser.py'

Files:
- ./samples.txt
    File that will contain your samples (strings)
    Will be generated after `samples.save()`
- ./notes.json
    File that will contain your notes (keys:values)
    Will be generated after REPL exiting

"""
from parsers.imports import importcore as _importcore
core = _importcore('youtube')

from .parser import info
from .parser import main
from .parser import parser
from .parser import samples


note = lambda: vars(note)  # noqa: E731


from parsers.imports import shortcuts
shortcuts = shortcuts(fn=main, nb=note, pa=parser, ss=samples)

import atexit as _atexit
from parsers.storage.files import exit_handler as _exit_handler
_atexit.register(_exit_handler, note, file=core.constloc.SAMPLE_FILE.replace('samples', 'notes'))
