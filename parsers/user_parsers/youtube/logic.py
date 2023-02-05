# mypy: disable-error-code=attr-defined
"""
DownloadHandler functions:
```
    def simple(obj: KeyAttrValue | YouTube, dir) -> str
        ...
    def download_video(playlist: Playlist, dir, max_retries=5) -> str
        ...
    def download_audio_mp4(playlist: Playlist, *, dir, max_retries) -> None
        ...
    def download_audio_mp3(playlist: Playlist, *, dir, max_retries) -> None
        ...
```
Sample handlers:
```
    def main.<locals>.inner_main(samples: KeyAttrValue) -> str
        ...
    def simple(obj: KeyAttrValue | YouTube, dir) -> str
        ...

main(fkey: WhatToDownload | int = WhatToDownload.video_mp4) -> SampleHandlerFunc
    See main.__doc__ and main.<locals>.inner_main.__doc__
```

fmap:   dictionary specifying one or more integers as keys with
        their corresponding DownloadHandler functions as values

"""
import functools
import json
import os
import time
import typing as _t
from enum import Enum, auto
from inspect import getfullargspec

# https://pytube.io/en/latest/api.html#playlist-object
from pytube import Playlist, YouTube
# https://ffmpy.readthedocs.io/en/latest/
try:
    import ffmpy
except ModuleNotFoundError:
    from parsers.imports import warn_object_not_found
    warn_object_not_found('ffmpy')

from parsers.datatypes import KeyAttrValue
from parsers.exceptions import BadResponse
from parsers.format.colors import Colors

from .constants import constant_locals as const

SampleHandlerFunc = _t.Callable[[KeyAttrValue], str]
TrackName: _t.TypeAlias = str
DownloadHandler = _t.Callable  # [[Any,
# DefaultNamedArg(Any, 'dir'), DefaultNamedArg(Any, 'max_retries')], List[str]]
fmap: dict[int, DownloadHandler]

SAVED_PLAYLIST_DIR = const.PARSED_DIR + '/' + const.PLAYLIST_ID
SAVED_VIDEO_DIR = const.PARSED_DIR + '/' + const.VIDEO_ID


def download_videos(playlist: Playlist, dir=SAVED_PLAYLIST_DIR, max_retries=5) -> str:
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


def get_post_process_info(playlist: Playlist, content='unknown') -> str:
    """Return message information after downloading playlist"""
    return (
        f'{len(playlist)} {content}(s) successfullly downloaded '
        f'from {playlist.playlist_url}\n'
    ) + ls_downloaded() + remind_optional_move()


def ls_downloaded(dir=SAVED_PLAYLIST_DIR) -> str:
    return '\n\t'.join(os.listdir(dir))


def remind_optional_move(
    playlist_id=const.PLAYLIST_ID,
    move_script=const.MOVE_SCRIPT,
    playlists=const.PLAYLISTS
) -> str:
    """Return message hint to move resources"""
    with open(playlists) as fh:
        j = json.loads(fh.read())

    playlist_key = key_by_value(j, playlist_id)
    destination_dir = j.get(f'{playlist_key}_mv_to')
    return (
        f"\nMove sources to {destination_dir} (with 'jq'):\n"
        f'\t{os.path.relpath(move_script)} {playlist_key}'
        if playlist_key and destination_dir else ''
    )


def simple(obj: KeyAttrValue | YouTube, dir=const.PARSED_DIR) -> str:
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


def download_audio(
    pytube_obj: Playlist | YouTube,
    convert_mp3: bool,
    word_separator: str = '_',
    dir: str = None,
    max_retries: int = 10,
) -> list[TrackName]:
    """Download audio from YouTube to `dir`.

    `convert_mp3`:
        a flag to start `ffmpeg` video converter

    """
    is_playlist = isinstance(pytube_obj, Playlist)
    dir = dir or SAVED_PLAYLIST_DIR if is_playlist else SAVED_VIDEO_DIR
    downloaded_track_names = []
    for video in (pytube_obj.videos if is_playlist else [pytube_obj]):

        request_problem = True
        while request_problem:
            try:
                audio = video.streams.get_audio_only()
                request_problem = False
            except BadResponse as e:
                print(e, f'\n{Colors.YELLOW}sleep 10s...{Colors.NC}')
                time.sleep(10)

        track_name = video.title.replace(' ', word_separator) + '.mp4'
        audio.download(dir, filename=track_name, max_retries=max_retries)  # pyright: ignore

        if convert_mp3:
            track_name = convert_to_mp3(f'{dir}/', track_name)
            downloaded_track_names.append(f'{dir}/{track_name}')
        else:
            downloaded_track_names.append(f'{dir}/{track_name}')
    return downloaded_track_names


def update_kwdefaults(func: DownloadHandler) -> _t.Callable:
    """Return nested function object with `func` kwargs in __kwdefaults__

    The nested function returns `func(*args, **kwargs)`
    `func`: Co-execute `download_audio` function.

    ```
    assert inspect.fullargspec(func).kwonlydefaults is not None, '''

        The decorated function must have required keyword-only arguments:
        'dir' and 'max_retries', that will be overwritten when passed
        parameters with the same names have values.'''

    >>> @update_kwdefaults
    ... def download_all_youtube(pytube_obj, *, dir=..., max_retries=...):
    ...    ...                            #  ^
    ```
    """
    @functools.wraps(func)
    def inner_scip_key_if_value_none(*args, **kwargs):
        fullargspec = getfullargspec(func)
        kwonlydefaults = fullargspec.kwonlydefaults
        assert isinstance(kwonlydefaults, dict), (fullargspec, 'REREAD DOCSTRING')
        # 2-tuple contaning args and updated kwargs of the func (rr: for repl reuse)
        inner_scip_key_if_value_none.rr = args, {**kwonlydefaults, **kwargs}
        inner_scip_key_if_value_none.__kwdefaults__ = kwargs
        return func(*args, **kwargs)

    return inner_scip_key_if_value_none


@update_kwdefaults
def download_audio_mp4(pytube_obj, *, dir=None, max_retries=None) -> list[TrackName]:
    """Co-ex `download_audio` to download the audio(s) from YouTube in mp4 format"""
    optianal_kwargs = download_audio_mp4.__kwdefaults__
    return download_audio(pytube_obj, convert_mp3=False, **optianal_kwargs)


@update_kwdefaults
def download_audio_mp3(pytube_obj, *, dir=None, max_retries=None) -> list[TrackName]:
    """Co-ex `download_audio` to download the audio(s) from YouTube in mp3 format.

    Requires ffmpy to convert the mp4 to mp3!
        - `pip install ffmpy`
        - or uncomment parsers/user_parsers/youtube/requirements.txt

    """
    optianal_kwargs = download_audio_mp3.__kwdefaults__
    return download_audio(pytube_obj, convert_mp3=True, **optianal_kwargs)


def convert_to_mp3(dir, basename: str) -> str:
    """ffmpeg -i `basename`.mp4 `basename`.mp3"""
    new_filename = basename.replace('.mp4', '.mp3')
    try:
        print(
            f'Converting {Colors.YELLOW}{basename}{Colors.NC}'
            f' to {Colors.YELLOW}{new_filename}{Colors.NC}...',
            end='\t'
        )
        ffmpy.FFmpeg(
            inputs={dir + basename: None},
            outputs={dir + new_filename: None},
        ).run()
        print(f'{Colors.BLUE}[converted]{Colors.NC}')
    except ffmpy.FFRuntimeError as e:
        print(e)
    return new_filename


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
    # Will be run fmap[key or fkey]
    inner_main.key = 0
    inner_main.help = functools.partial(
        print,
        (main.__doc__, inner_main.__doc__)
    )

    return inner_main
