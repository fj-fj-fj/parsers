"""
Usage:

    For download playlists:
        1. PLAYLIST_ID: str = <DESIRED PLAYLIST ID>
        2. PARAMS = PARAMS_PLAYLIST_ID
        * Downloaded will be into './data/youtube/<DESIRED PLAYLIST ID>'

    For download one video/audio:
        1. VIDEO_ID: str = <DESIRED VIDEO ID>
        2. PARAMS = PARAMS_VIDEO_ID
        * Downloaded will be into './data/youtube/<DESIRED VIDEO ID>'

    For downloading into './data/youtube/'
        1. URL: str = <FULL URL>

"""
from types import SimpleNamespace as _namespace

from parsers.constants import Constant as _base

_URL = URL = 'https://youtube.com'

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

# Checked by `curl`=======================================
# The block of code below has been automatically generated
# Delete condition or reasign `URL`
# if 301 not in range(200, 400):
#     URL = _base.URL.HTTPBIN_ORG
# ========================================================


# # -------------------- with pytube.Playlist
#
# ----------------------------- playlist?list
PARAMS_PLAYLIST, PLAYLIST_ID = '/playlist?list=', ''
#
_test = 'PL6plRXMq5RADf1Jore6YlgX9tIKau9PIY'
# who(1st/2nd name)_about_nvidoes
AK_PYTHON_12 = 'PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
DK_LINUX_12 = 'PLHHm04DXWzeKZycf_ZuBgxWdVBnrjE_mj'
DK_BASICS_12 = 'PLHHm04DXWzeKuhdGFHSEWDpdgoYpjPptR'
AS_NETWORKS_56 = 'PLtPJ9lKvJ4oiNMvYbOzCmWy6cRzYAh9B1'
# PLAYLIST_ID = AK_PYTHON_12
# PLAYLIST_ID = DK_LINUX_12
# PLAYLIST_ID = DK_BASICS_12
# PLAYLIST_ID = AS_NETWORKS_56
# ...
PLAYLIST_ID = _test
PARAMS_PLAYLIST_ID = PARAMS_PLAYLIST + PLAYLIST_ID


# # --------------------- with pytube.YouTube
#
# ------------------------------------ shorts
PARAMS_SHORTS, SHORTS_ID = '/shorts/', ''
#
ITS_LIKE_THAT = 'v742rQOimgY'
# ...
SHORTS_ID = ITS_LIKE_THAT
PARAMS_SHORTS_ID = PARAMS_SHORTS + SHORTS_ID
#
# ----------------------------------- watch?v
PARAMS_WATCH, VIDEO_ID = '/watch?v=', ''
#
_test = 'RcenQ6CR_zM'
MUSIC_DJENT_10H = 'nBVwveVXkWs'
# VIDEO_ID = MUSIC_DJENT_10H
# ...
VIDEO_ID = _test
PARAMS_WATCH_ID = PARAMS_WATCH + VIDEO_ID


# # --------------------------- BUILD THE URL
#
YOUTUBE_URL, PARAMS = URL, ''
# PARAMS = PARAMS_PLAYLIST_ID
# PARAMS = PARAMS_SHORTS_ID
PARAMS = PARAMS_WATCH_ID
# ...
YOUTUBE_URL += PARAMS
# -------------------------------------------

if not PARAMS:
    from parsers.exceptions import URLError
    URLError.set_tracebacklimit(0)
    goto = f"\a\n\tGOTO: '{__file__}" "{add PARAMS}'"
    raise URLError(f'Parameters are required to download video(s)\n{goto}\n')


# --------------------------- COLLECT EXPORTS
constant_locals = _namespace(
    # parsers.constants.Constant
    base=_base,

    URL=YOUTUBE_URL,
    PLAYLIST_ID=PLAYLIST_ID,
    VIDEO_ID=VIDEO_ID,
    SHORTS_ID=SHORTS_ID,
    URL_WITHOUT_PARAMS=_URL,
    PARAMS=PARAMS,
    # Flags
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    # TODO: ? PYTUBE_OBJ = Playlist | YouTube
    # Files
    PARSED_DIR=PARSED_DIR,
    SAMPLE_FILE=SAMPLE_FILE,
    PLAYLISTS=PLAYLISTS,
    MOVE_SCRIPT=MOVE_SCRIPT,
)
