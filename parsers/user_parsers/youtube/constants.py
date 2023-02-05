# flake8: noqa E262
# pyright: reportUnboundVariable=false
"""This module is a set of constants and a settings file.

Usage:
    For download playlist:
        1. _playlist_id = <PLAYLIST-ID>
        1. uncomment `PLAYLIST_ID`
        2. uncomment `PARAMS = PARAMS_PLAYLIST_ID`

    For download one video/audio:
        For download '/shorts/':
            1. _shorts_id = <SHORTS-ID>
            2. uncomment `SHORTS_ID`
            3. uncomment `PARAMS = PARAMS_SHORTS_ID`
        For download '/watch?v=':
            1. _video_id = <VIDEO-ID>
            2. uncomment `VIDEO_ID`
            3. uncomment `PARAMS = PARAMS_WATCH_ID`

* Downloaded will be in './data/youtube/'

Tab-separeted-constants will help you quickly find the settings you need.

"""
__all__ = ['constant_locals']
import typing as _t
from types import SimpleNamespace as _namespace

from parsers.constants import Constant as _base

URL: _t.Final = 'https://youtube.com'

# Directory for storing final data
PARSED_DIR = F'{_base.DIR.PARSED_DATA}youtube'
# File to store samples for extracting raw data
SAMPLE_FILE = F'{_base.DIR.USER_PARSERS}youtube/samples.txt'
# File to store playlist IDs mapped destination dirs
PLAYLISTS = F'{_base.DIR.USER_PARSERS}youtube/playlists'
# Script to move downloaded videos
MOVE_SCRIPT = F'{_base.DIR.USER_PARSERS}youtube/move.sh'
# Display result to the screen
PRINT_TO_STDOUT = True


if True:  # Read-only
    PARAMS_PLAYLIST, PLAYLIST_ID = '/playlist?list=', ''
    PARAMS_SHORTS, SHORTS_ID = '/shorts/', ''
    PARAMS_WATCH, VIDEO_ID = '/watch?v=', ''
    YOUTUBE_URL, PARAMS = URL, ''


if 'pytube.Playlist':  # than uncomment PLAYLIST_ID
    test = 'PL6plRXMq5RADf1Jore6YlgX9tIKau9PIY'
    AK_PYTHON_12 = 'PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
    DK_LINUX_12 = 'PLHHm04DXWzeKZycf_ZuBgxWdVBnrjE_mj'
    DK_BASICS_12 = 'PLHHm04DXWzeKuhdGFHSEWDpdgoYpjPptR'
    AS_NETWORKS_56 = 'PLtPJ9lKvJ4oiNMvYbOzCmWy6cRzYAh9B1'
    _playlist_id = 'PLKacnqDKwqBQeYSZldTBrRHWYNJxSiJJ6'
    # PLAYLIST_ID: _t.Final = _playlist_id  #                      <<--  check
    PARAMS_PLAYLIST_ID: _t.Final = PARAMS_PLAYLIST + PLAYLIST_ID


if 'pytube.YouTube':
    ## if /shorts/ than uncomment SHORTS_ID
    ITS_LIKE_THAT = 'v742rQOimgY'
    _shorts_id = ITS_LIKE_THAT
    # SHORTS_ID: _t.Final = _shorts_id  #                         <<---  check
    PARAMS_SHORTS_ID: _t.Final = PARAMS_SHORTS + SHORTS_ID

    ## if /watch?v= than uncomment VIDEO_ID
    MUSIC_DJENT_10H = 'nBVwveVXkWs'
    _video_id = '36HrYaGT6Cw'
    # VIDEO_ID: _t.Final = _video_id  #                           <<---  check
    PARAMS_WATCH_ID: _t.Final = PARAMS_WATCH + VIDEO_ID


## Make suitable PARAMS available
# PARAMS = PARAMS_PLAYLIST_ID  # uncomment if playlist            <<---  check
# PARAMS = PARAMS_SHORTS_ID  # uncomment if shorts                <<---  check
# PARAMS = PARAMS_WATCH_ID   # uncomment if watch                 <<---  check

if not PARAMS:
    from parsers.exceptions import URLError
    URLError.set_tracebacklimit(0)
    goto = f"\a\n\tGOTO: '{__file__}" "{add PARAMS}'"
    raise URLError(f'Parameters are required to download video(s)\n{goto}\n')


YOUTUBE_URL += PARAMS  # Final

constant_locals = _namespace(
    # parsers.constants.Constant
    base=_base,
    # URL
    URL=YOUTUBE_URL,
    PARAMS=PARAMS,
    URL_WITHOUT_PARAMS=URL,
    # Flags
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    # Files
    PARSED_DIR=PARSED_DIR,
    SAMPLE_FILE=SAMPLE_FILE,
    PLAYLISTS=PLAYLISTS,
    MOVE_SCRIPT=MOVE_SCRIPT,

    # Checking
    PLAYLIST_ID=PLAYLIST_ID,
    SHORTS_ID=SHORTS_ID,
    VIDEO_ID=VIDEO_ID,
    PARAMS_PLAYLIST=PARAMS_PLAYLIST,
    PARAMS_SHORTS=PARAMS_SHORTS,
    PARAMS_WATCH=PARAMS_WATCH,
)
