from types import SimpleNamespace as _SimpleNamespace

from .constants import (
    CHROMEDRIVER as _driver,
    CHROMEDRIVER_LOG_FILE as _log_file,
)

_chromedriver_config = {
    'driver': _driver,
    'log_file': _log_file,
}

chromedriver_config = _SimpleNamespace(**_chromedriver_config)
