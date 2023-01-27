"""
Download sources:
    def simple(obj: KeyAttrValue | YouTube, dir) -> str
        ...
    def download_video(playlist: Playlist, dir, max_retries=5) -> str
        ...
    def download_audio_mp4(playlist: Playlist, dir) -> str
        ...
    def download_audio_mp3(playlist: Playlist, dir) -> str
        ...

Sample handler:
    def main.<locals>.inner_main(samples: KeyAttrValue) -> str
        ...
    def simple(obj: KeyAttrValue | YouTube, dir) -> str
        ...

main(fkey: WhatToDownload | int = WhatToDownload.video_mp4) -> SampleHandlerFunc
    See main.__doc__ and main.<locals>.inner_main.__doc__

"""
# mypy: disable-error-code=attr-defined
import functools
import json
import os
import time
import typing as _t
from enum import Enum, auto

# https://pytube.io/en/latest/api.html#playlist-object
from pytube import Playlist, YouTube
# https://ffmpy.readthedocs.io/en/latest/
try:
    import ffmpy
except ModuleNotFoundError:
    pass

from parsers.datatypes import KeyAttrValue

from .constants import PARSED_DIR as GRANDPARENT, PLAYLIST_ID as PARENT_NAME
from .constants import PLAYLISTS as PLAYLISTS_JSON, MOVE_SCRIPT, PLAYLIST_ID

SampleHandlerFunc = _t.Callable[[KeyAttrValue], str]
DownloadHandler = _t.Callable
fmap: dict[int, DownloadHandler]

DOWNLOAD_DIR = GRANDPARENT + '/' + PARENT_NAME


def download_videos(playlist: Playlist, dir=DOWNLOAD_DIR, max_retries=5) -> str:
    """Download YouTube playlist in mp4 format"""
    for number, video in enumerate(playlist.videos, 1):
        video.streams.filter(
            type='video',
            # https://ottverse.com/mpeg-dash-video-streaming-the-complete-guide/
            progressive=True,
            file_extension='mp4',
        ).order_by('resolution')\
            .desc()\
            .first()\
            .download(  # pyright: ignore [reportOptionalMemberAccess]
                dir,
                filename_prefix=f'{number:02}. ',
                max_retries=max_retries,
        )
    return get_post_process_info(playlist, 'video')


def download_audio_mp4(playlist: Playlist, dir=DOWNLOAD_DIR) -> str:
    """Download the YouTube playlist in mp4 but the only audio format"""
    for video in playlist.videos:
        audio = video.streams.get_audio_only()
        audio.download(dir)  # pyright: ignore [reportOptionalMemberAccess]
    return get_post_process_info(playlist, 'audio')


def download_audio_mp3(playlist: Playlist, dir=DOWNLOAD_DIR) -> str:
    """Download the YouTube playlist in mp4 but the only audio format.

    Install ffmpy to convert the mp4 to mp3
        - `pip install ffmpy`
        - or uncomment parsers/user_parsers/youtube/requirements.txt

    """
    for video in playlist.videos:
        audio = video.streams.get_audio_only()
        audio.download(dir)  # pyright: ignore [reportOptionalMemberAccess]
        video_title = video.title
        new_filename = f'{video_title}.mp3'
        default_filename = f'{video_title}.mp4'
        print(f'Convert {default_filename} to {new_filename}')
        ff = ffmpy.FFmpeg(
            inputs={default_filename: None},
            outputs={new_filename: None}
        )
        ff.run()
    return get_post_process_info(playlist, 'audio')


def simple(obj: KeyAttrValue | YouTube, dir=GRANDPARENT) -> str:
    """Download Youtube video (mp4).

        >>> from pytube import YouTube as yt
        >>> path = simple(yt('https://www.youtube.com/shorts/v742rQOimgY'))
        >>> assert path is simple.dir  # Check downloaded there
        >>> simple.yt.author
        >>> 'Диджитализируй!'
        >>> simple.yt.title
        >>> 'Всё так!'  # да

    """
    # attr_value: list[<pytube.__main__.YouTube object: videoId=v742rQOimgY>]
    yt, = obj.attr_value if isinstance(obj, KeyAttrValue) else [obj]
    simple.yt, simple.dir = yt, dir
    assert isinstance(yt, YouTube), (yt, vars(yt))
    return yt.streams.get_highest_resolution().download(dir)  # pyright: ignore


def get_post_process_info(playlist: Playlist, content='unknown') -> str:
    return (
        f'{len(playlist)} {content}(s) successfullly downloaded '
        f'from {playlist.playlist_url}\n'
    ) + list_downloaded() + remind_optional_move()


def list_downloaded(dir=DOWNLOAD_DIR) -> str:
    return '\n\t'.join(os.listdir(dir))


def remind_optional_move(
    playlist_id=PLAYLIST_ID,
    move_script=MOVE_SCRIPT,
    playlists=PLAYLISTS_JSON
) -> str:
    with open(playlists) as fh:
        j = json.loads(fh.read())

    playlist_key = key_by_value(j, playlist_id)
    destination_dir = j.get(f'{playlist_key}_mv_to')
    return (
        f"\nMove sources to {destination_dir} (with 'jq'):\n"
        f'\t{os.path.relpath(move_script)} {playlist_key}'
        if playlist_key and destination_dir else ''
    )


def key_by_value(mapping: dict, value: _t.Any) -> _t.Hashable | None:
    return {v: k for k, v in mapping.items()}.get(value)


def hms_time(secs: float) -> str:
    """Return human-friendly time by `secs`"""
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return f'{hours:.0f}:{mins:.0f}:{secs:n}'


class WhatToDownload(Enum):
    playlist = auto()
    audio_mp4 = auto()
    audio_mp3 = auto()


fmap = {1: download_videos, 2: download_audio_mp4, 3: download_audio_mp3}
# mapf = lambda f_number: lambda sample: fmap[f_number](*sample.attr_value)


def main(fkey: WhatToDownload | int = WhatToDownload.playlist) -> SampleHandlerFunc:
    """Choose what to download:

    `main(1)` -> `SampleHandlerFunc` (to download mp4 videos)

    `main(2)` -> `SampleHandlerFunc` (to download mp4 audio)

    `main(3)` -> `SampleHandlerFunc` (to download mp3 audio)

    """
    assert isinstance(fkey, int) or issubclass(type(fkey), Enum)
    fkey = fkey if isinstance(fkey, int) else fkey.value

    def inner_main(samples: KeyAttrValue) -> str:
        """Download playlist (API)

        Check current download function:
            >>> inner_main.func
        Check current download func key:
            >>> inner_main.fkey
        Check what download funcs are available:
            >>> inner_main.fmap
        Change download function:
            >>> inner_main.key = <fmap key>
            >>> parser.logic = inner_main
        Check total running time (secs):
            >>> inner_main.elapsed
        Check total running time (H-friendly):
            >>> inner_main.ELAPSED
        Display the key operation help message:
            >>> inner_main.help()

        Happy downloading!
        """
        playlist, = samples.attr_value
        key = inner_main.key or fkey
        assert isinstance(key, int)
        func: DownloadHandler = fmap[key]
        inner_main.func = func

        start = time.perf_counter()
        result = func(playlist)
        elapsed = time.perf_counter() - start

        inner_main.elapsed = elapsed
        inner_main.ELAPSED = hms_time(elapsed)

        print('\a')
        return result

    # Interactive mode access
    inner_main.fmap = fmap
    inner_main.fkey = fkey
    inner_main.key = 0
    inner_main.help = functools.partial(
        print,
        (main.__doc__, inner_main.__doc__)
    )

    return inner_main
