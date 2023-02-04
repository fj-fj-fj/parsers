__all__ = [
    'DEBUG_ALL',
    'DEBUG_ERR',
    'DEBUG_OUT',
    'LOG',
    'NOTES',
    'PARSED_DATA',
    'PARSERS',
    'PROJECT_DIR',
    'SAMPLE',
    'USER_PARSERS',
    'USER_AGENTS',
    'Dir',
    'File',
]
import os as _os
import typing as _t

PROJECT_DIR: _t.Final = _os.getenv('PROJECT_DIR', '../..')

PARSERS: _t.Final = F'{PROJECT_DIR}/parsers/'
USER_PARSERS: _t.Final = F'{PARSERS}user_parsers/'
PARSED_DATA: _t.Final = F'{PROJECT_DIR}/data/'

USER_AGENTS = F'{PROJECT_DIR}/useragents.txt'
SAMPLE = F'{PROJECT_DIR}/samples.txt'
NOTES = F'{PROJECT_DIR}/notes.txt'

LOG = F'{PROJECT_DIR}/log/'
DEBUG_OUT = F'{LOG}out.log'
DEBUG_ERR = F'{LOG}err.log'
DEBUG_ALL = F'{LOG}all.log'


class Dir(_t.NamedTuple):
    PROJECT_DIR: str = PROJECT_DIR
    PARSERS: str = PARSERS
    USER_PARSERS: str = USER_PARSERS
    PARSED_DATA: str = PARSED_DATA
    LOG: str = LOG


class File(_t.NamedTuple):
    USER_AGENTS: str = USER_AGENTS
    SAMPLE: str = SAMPLE
    NOTES: str = NOTES
    DEBUG_OUT: str = DEBUG_OUT
    DEBUG_ERR: str = DEBUG_ERR
    DEBUG_ALL: str = DEBUG_ALL
