#!/usr/bin/env python
# mypy: ignore-errors
"""
Usage:

    First start writing CSS selectors
    ---------------------------------

    >>> parser.go
    >>> soup.select(<any selector>)
    >>> ss.add(<correct selector>)
    >>> # ... See more EXAMPLE.md
    >>> ss.save()
    >>> q()

    Now that you have a list of samples, just run this parser
    ---------------------------------------------------------

    Find parsed data in /mnt/c/dev/fj-fj-fj/parsers/data/<parser>
    They are yours.

"""
import sys
from pydoc import pager

if is_script := __name__ == '__main__':
    __package__ = 'parsers.user_parsers.merge_checker'
    sys.path.insert(0, sys.path[0] + 3 * '/..')

from ...constants import Constant
from ...datatypes import EXIT_CODE, Sample
from ...handlers import Parser
from ...imports import ModuleDocstring as info, snoop

from .logic import main as sample_handler
from .constants import constant_locals as constloc

URL = constloc.URL or input(Constant.PROMPT.ENTER_URL_OR_FALSE)

samples = Sample(file=constloc.SAMPLE_FILE)
parser = Parser(URL, constloc.PARSED_DIR, samples)


# @snoop
def main(display=constloc.PRINT_TO_STDOUT) -> EXIT_CODE:
    """Parse and save.

    When `display` is True, parsed data will down to stdout.
    Return exit code.
    """
    parser.logic = sample_handler
    parsed = parser.go
    if display and not parsed.fail:
        pager(str(parsed.data))
    return parsed.status_code


if is_script and not sys.flags.interactive:
    sys.exit(main())

info = info(__doc__)
