import atexit
import readline
import os

PYTHON_LOG_FILE = f"{os.environ['PROJECT_DIR']}/log/.python_history"

def set_interactive_mode():
    os.environ['PYTHONINSPECT'] = 'True'


def register_python_history_file(name: str = PYTHON_LOG_FILE):
    atexit.register(lambda: readline.write_history_file(name))


history = readline.get_history_item
current_history_length = readline.get_current_history_length()
# as `history | top -<n>`
top = lambda n: [history(command) for command in range(n)]
# as `history | tail -<n>`
tail = lambda n: [
    history(current_history_length - command) for command in range(n, 0, -1)
]
