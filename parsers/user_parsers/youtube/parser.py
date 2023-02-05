#!/usr/bin/env python
# flake8: noqa E262
# mypy: ignore-errors
"""
To download a single video, uncomment it:
    # parser.handler.request_handler.get = use.yt
    # sample_handler = simple

To download the playlist, find and uncomment this:
    # parser.handler.request_handler.get = use.pl
    # sample_handler = sample_handler()

To download audio:
    # sample_handler = sample_handler(WhatToDownload.audio_mp4)
    or
    # sample_handler = sample_handler(WhatToDownload.audio_mp3)

"""
import sys
from pydoc import pager

from pytube.exceptions import RegexMatchError

if is_script := __name__ == '__main__':
    __package__ = 'parsers.user_parsers.youtube'
    sys.path.insert(0, sys.path[0] + 3 * '/..')

from ...constants import Constant
from ...datatypes import EXIT_CODE, Sample
from ...handlers import Parser
from ...imports import ModuleDocstring as info, snoop

from .constants import constant_locals as constloc
from .logic import WhatToDownload
from .logic import main as sample_handler, simple

URL = constloc.URL or input(Constant.PROMPT.ENTER_URL_OR_FALSE)

samples = Sample(file=constloc.SAMPLE_FILE)
parser = Parser(URL, constloc.PARSED_DIR, samples)


class use:
    """Use PlayList or Youtube instead of requests.get"""
    from pytube import YouTube as yt
    from pytube import Playlist as pl


# # Make request with:
# parser.handler.request_handler.get = use.pl  #                   <<--- check
# parser.handler.request_handler.get = use.yt  #                   <<--- check
# TODO: sys.argv[pl or yt, sample_handler.fkey]

# # Handle samples with:
# sample_handler = simple  #                                       <<--- check
# sample_handler = sample_handler()  #                             <<--- check
# sample_handler = sample_handler(WhatToDownload.audio_mp4)  #     <<--- check
# sample_handler = sample_handler(WhatToDownload.audio_mp3)  #     <<--- check


def main(display=constloc.PRINT_TO_STDOUT) -> EXIT_CODE:
    """Parse and save.

    When `display` is True, parsed data will down to stdout.
    Return exit code.
    """
    parser.logic = sample_handler
    try:
        parsed = parser.go
    except RegexMatchError as rme:
        from parsers.exceptions import URLError
        from parsers.format.colors import Colors
        raise URLError(
            f'\v\t{Colors.RED}{constloc.URL}{Colors.NC}{{ ? }}'
        ) from rme
    else:
        if display and not parsed.fail:
            pager(str(parsed.data))
    return parsed.status_code


if __debug__:
    from parsers.exceptions import makeassert

    # Comment/uncomment checking
    if parser.handler.request_handler.get == use.pl:
        # fail if '/playlist?list=' not in target URL
        makeassert(constloc.PARAMS_PLAYLIST, 'in', constloc.PARAMS)
        # fail if trying to download playlist with `simple`
        makeassert(sample_handler.__name__, '!=', simple.__name__)
    if parser.handler.request_handler.get == use.yt:
        # fail if '/playlist?list=' in target URL
        makeassert(constloc.PARAMS_PLAYLIST, 'not in', constloc.PARAMS)
        # fail if sample_handler(fkey=WhatToDownload.playlist)
        makeassert(sample_handler.__dict__.get('fkey'), '!=', 1)

if is_script and not sys.flags.interactive:
    sys.exit(main())

info = info(__doc__)
