from pytube import Playlist

from parsers.datatypes import KeyAttrValue
from .constants import PARSED_DIR as GRANDPARENT, PLAYLIST_ID as PARENT_NAME

DOWNLOAD_DIR = GRANDPARENT + '/' + PARENT_NAME


def _main(playlist: Playlist, dir=DOWNLOAD_DIR) -> None:
    """https://pytube.io/en/latest/api.html#playlist-object"""
    for video in playlist.videos:
        video.streams.filter(
            type='video',
            progressive=True,
            file_extension='mp4',
        ).order_by('resolution')\
            .desc()\
            .first()\
            .download(dir)  # pyright: ignore [reportOptionalMemberAccess]


def main(samples: KeyAttrValue) -> None:
    """Handle samples. (API)"""
    playlist, = samples.attr_value
    _main(playlist=playlist)
