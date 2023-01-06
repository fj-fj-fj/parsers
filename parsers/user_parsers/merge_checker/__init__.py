#!/usr/bin/env python
# mypy: ignore-errors
"""
Modules:
- logic
    'parsers.user_parsers.merge_checker.logic' from './merge_checker/logic.py'
- constatns
    parsers.user_parsers.merge_checker.constants' from './merge_checker/constats.py'
- parser (alias core)
    parsers.user_parsers.merge_checker.parser' from './merge_checker/parser.py'

Functions:
- main
    'parsers.user_parsers.merge_checker.parser.main' function from './merge_checker/parser.py'
- shortcuts
    'parsers.imports.shortcuts.<locals>._shortcuts'
- note
    (lambda) Simple dict-like container
    Use ad-hoc attributes to hodl smth
    Will be automatically saved to ./notes.json

Classes:
- info
    'parsers.imports.ModuleDocstring' instance from './merge_checker/parser.py'
- parser
    'parsers.handlers.Parser' instance from './merge_checker/parser.py'
- samples
    'parsers.datatypes.Sample' list-like instance from './merge_checker/parser.py'

Files:
- ./samples.txt
    File that will contain your samples (strings)
    Will be generated after `samples.save()`
- ./notes.json
    File that will contain your notes (keys:values)
    Will be generated after REPL exiting

"""
from parsers.imports import importcore as _importcore
core = _importcore('merge_checker')

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
