import atexit as _atexit, os as _os, readline as _readline

PYTHON_LOG_FILE = f'{_os.getcwd()}/parsers/zvk/.python_history'


def set_interactive_mode():
    _os.environ['PYTHONINSPECT'] = 'True'


def register_python_history_file(name: str = PYTHON_LOG_FILE):
    _atexit.register(lambda: _readline.write_history_file(name))


history = _readline.get_history_item
current_history_length = _readline.get_current_history_length()
# as `history | top -<n>`
top = lambda n: [history(command) for command in range(n)]
# as `history | tail -<n>`
tail = lambda n: [
    history(current_history_length - command) for command in range(n, 0, -1)
]

# Make `exit` work without `()`
type(exit).__repr__ = type(exit).__call__
q = exit  # `exit` shortcat
