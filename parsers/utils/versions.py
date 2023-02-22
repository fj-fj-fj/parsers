__all__ = [
    'get_chrome_version',
    'get_linux_chrome_version',
    'get_win_chrome_version',
    'get_cmd_chrome_version',
    'get_pwsh_chrome_version',
]
import subprocess as _subprocess  # nosec B404
import typing as _t

DEFAULT_ENCODING = 'UTF-8'
HKCU_CHROME_BLBEACON = R'HKEY_CURRENT_USER\Software\Google\chrome\BLBeacon'

CHROME_EXECUTABLE = (
    'google-chrome',
    'google-chrome-stable',
    'google-chrome-beta',
    'google-chrome-dev',
    'chromium-browser',
    'chromium'
)


def get_chrome_version(platform: _t.Literal['linux', 'win']) -> str | None:
    r"""Return version of chrome installed on client.

    Implemented only:
        linux (which google-chrome)
        win (Get-ItemProperty path\to\BLBeacon)

    """
    return {
        'linux': get_linux_chrome_version,
        'win': get_win_chrome_version,
        'wsl': get_win_chrome_version,
    }.get(platform, lambda: None)()


def get_linux_chrome_version() -> str | None:
    path = None
    try:
        _subprocess.check_output(  # nosec B603 B607
            ' '.join([
                'which',
                *CHROME_EXECUTABLE,
                'error!'
            ]),
            shell=True,  # nosec B602
        )
    except _subprocess.CalledProcessError as e:
        # Select first path from `which` results (if exist)
        path = (out := e.output) and out.decode(DEFAULT_ENCODING).strip().split()[0] or None
    if not path:
        return None

    with _subprocess.Popen([  # nosec B603 B607
        path,
        '--version'
    ],
        stdout=_subprocess.PIPE
    ) as proc:
        assert proc.stdout, (proc.stdout, vars())
        return (
            proc.stdout.read()
            .decode(DEFAULT_ENCODING)
            .replace('Chromium', '')
            .replace('Google Chrome', '')
            .strip()
        )


def get_win_chrome_version() -> str | None:
    return get_cmd_chrome_version() or get_pwsh_chrome_version()


def get_cmd_chrome_version() -> str | None:
    output = _subprocess.Popen([  # nosec B603 B607
        'cmd.exe',
        '/c'
        'REG',
        'QUERY',
        HKCU_CHROME_BLBEACON,
        '/v',
        'version'
    ],
        stdin=_subprocess.DEVNULL,
        stdout=_subprocess.PIPE,
        stderr=_subprocess.DEVNULL,
    ).communicate()
    if output and output[0]:
        return output[0].decode(DEFAULT_ENCODING).strip().split()[-1]


def get_pwsh_chrome_version() -> str | None:
    output = _subprocess.Popen([  # nosec B603 B607
        'powershell.exe',
        '-command',
        f'$(Get-ItemProperty -Path Registry::{HKCU_CHROME_BLBEACON}).version',
    ],
        stdin=_subprocess.PIPE,
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
    ).communicate()
    if output and output[0]:
        return output[0].decode(DEFAULT_ENCODING).strip()
