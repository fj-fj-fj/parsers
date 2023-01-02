"""The 'times' module contains tools for sleep, timeout, etc."""

__all__ = (
    'Timeout',
    'set_random_timeout',
    'set_timeout',
)
import typing as _t
from random import uniform as _uniform

from parsers.constants import Constant as _Constant

_TimeoutType: _t.TypeAlias = float | tuple[float, ...] | None

class Timeout:

    @staticmethod
    def set_random_timeout(min_num: int = 20) -> _TimeoutType:
        """Return tuple with floats (random() * min_num)"""
        #  min_num: timeout cannot be set to a value less than or equal to 0
        #  urllib3/util/timeout.py, line 151, in _validate_timeout
        connection_timeout = _uniform(min_num / 2, min_num)
        read_timeout = _uniform(min_num, min_num * 2)
        return connection_timeout, read_timeout

    @staticmethod
    def set_timeout(const: _t.Type[_Constant] = _Constant, random: bool = True) -> _TimeoutType:
        """Return random timeout or constants.ConstantStorage.TIMEOUTS."""
        return Timeout.set_random_timeout() if random else const.TIMEOUTS


# Export Timeout methods as module-level functions
set_random_timeout = Timeout.set_random_timeout
set_timeout = Timeout.set_timeout
