def save(data: str, file: str, mode: str='w', log: bool=False):
    if log:
        print(f'Saving data to {file}...')
    with open(file, mode) as f:
        f.write(data)
    if log:
        print('  Saved successfully!')


def set_random_timeout(mnum: int=10) -> tuple[float, float]:
    """Return tuple with floats (random() * mnum)"""
    from random import random, uniform

    # while not Invalid timeout
    #   urllib3/util/timeout.py, line 151, in _validate_timeout
    #   timeout cannot be set to a value less than or equal to 0
    while all([
        connect_time_min := int(random() * mnum) > 3,
        connect_time_max := connect_time_min + int(random() * mnum) > 3,
        read_time_min := int(random() * mnum) > 5,
        read_time_max := read_time_min + int(random() * mnum) > 5,
    ]):
        connection_timeout = uniform(connect_time_min, connect_time_max)
        read_timeout = uniform(read_time_min, read_time_max)

    return connection_timeout, read_timeout


class classproperty(property):
    """Decorator @staticmethod & @property"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
