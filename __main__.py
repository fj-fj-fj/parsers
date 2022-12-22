#!/usr/bin/env python
"""Entry point.

Requires exactly one command-line argument <parser>.
"""
from parsers.imports import refresh


def entry():
    """Entry point.
    Returns the matched parser or exits with status 65
    """
    from parsers.imports import select_parser
    try:
        parser = select_parser()
    except Exception as ex:
        import os
        print(ex)
        os._exit(os.EX_DATAERR)
    return parser


__parser__ = entry()

if __import__('sys').flags.interactive:
    # import * from selected package into interactive shell
    exec(f'from {__parser__.__name__} import *; print(info)')
else:
    __parser__.main()
