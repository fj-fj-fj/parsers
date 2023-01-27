#!/usr/bin/env python
# mypy: ignore-errors
""""""
import sys
from pydoc import pager

if is_script := __name__ == '__main__':
    __package__ = 'parsers.user_parsers.youtube'
    sys.path.insert(0, sys.path[0] + 3 * '/..')

from ...constants import Constant
from ...datatypes import EXIT_CODE, Sample
from ...handlers import Parser
from ...imports import ModuleDocstring as info, snoop

from .constants import constant_locals as constloc
from .logic import main as sample_handler, simple

URL = constloc.URL or input(Constant.PROMPT.ENTER_URL_OR_FALSE)

samples = Sample(file=constloc.SAMPLE_FILE)
parser = Parser(URL, constloc.PARSED_DIR, samples)


class use:
    """Use PlayList or Youtube instead of requests.get"""
    from pytube import YouTube as yt
    from pytube import Playlist as pl

# Check .logic and select sample_handler
# - download playlist (videos/audios):
sample_handler = sample_handler()
parser.handler.request_handler.get = use.pl
# - download one video:
# sample_handler = simple
# parser.handler.request_handler.get = use.yt


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

# info = info(__doc__)
