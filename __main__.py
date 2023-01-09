#!/usr/bin/env python
"""Entry point.

Requires exactly one command-line argument <parser>.
"""
from parsers.imports import refresh


def entry():
    """Return the matched parser object"""
    from parsers.imports import select_parser
    parser = select_parser()
    return parser


__parser__ = entry()

if __import__('sys').flags.interactive:
    exec(f'from {__parser__.__name__} import *; print(info)')
else:
    __parser__.main()
