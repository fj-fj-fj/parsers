#!/usr/bin/env python
"""Entry point.

Requires exactly one command-line argument.

"""
from types import ModuleType


def select_parser() -> ModuleType:
    """Return mapped parser script by sys.argv or raise."""
    from importlib import import_module
    from sys import argv
    try:
        parser = argv[1]
    except IndexError:
        print('\t\033[1;31mYou forgot to enter the parser name!')
        print('\t\033[0;33mUsage: make run parser_name\033[0m')
        raise
    return import_module(f'parsers.user_parsers.{parser}')


def entry() -> None:
    """Entry point."""
    parser = select_parser()
    parser.main()


entry()
