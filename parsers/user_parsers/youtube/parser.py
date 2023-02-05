#!/usr/bin/env python
# mypy: ignore-errors
"""
Select sample handler
    See .logic.__doc__

Select GET request maker
    See use.__doc__

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


# # -*- GET request playlist:
# parser.handler.request_handler.get = use.pl
#
# # -*- GET request one video:
parser.handler.request_handler.get = use.yt

# # -*-  Download one video:
# sample_handler = simple
#
# # -*-  Download playlist (videos):
# sample_handler = sample_handler()
#
# # -*- Download one audio mp4:
# sample_handler = sample_handler(WhatToDownload.audio_mp4)
#
# # -*- Download one audio mp3:
sample_handler = sample_handler(WhatToDownload.audio_mp3)


# @snoop
def main(display=constloc.PRINT_TO_STDOUT) -> EXIT_CODE:
    """Parse and save.

    When `display` is True, parsed data will down to stdout.
    Return exit code.
    """
    parser.logic = sample_handler
    try:
        parsed = parser.go
    except RegexMatchError as _:
        from parsers.exceptions import URLError
        from parsers.format.colors import Colors
        raise URLError(
            f'\v\t{Colors.RED}{constloc.URL}{Colors.NC}{{'
            f'{Colors.YELLOW}params={constloc.PARAMS}{Colors.NC}?}}'
        ) from _
    else:
        if display and not parsed.fail:
            pager(str(parsed.data))
        return parsed.status_code


if __debug__:
    from parsers.exceptions import makeassert

    # Check compatibility settings
    if parser.handler.request_handler.get == use.pl:
        makeassert(constloc.PARAMS_PLAYLIST, 'in', constloc.PARAMS)
        makeassert(sample_handler.__name__,'!=', simple.__name__)
    if parser.handler.request_handler.get == use.yt:
        makeassert(constloc.PARAMS_PLAYLIST, 'not in', constloc.PARAMS)

if is_script and not sys.flags.interactive:
    sys.exit(main())

# info = info(__doc__)
