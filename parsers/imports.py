from functools import wraps as _wraps

try:
    import snoop
except ModuleNotFoundError:
    def snoop(func):
        """Decorator stub for `snoop`

        `pip install snoop`
        see https://github.com/alexmojaki/snoop

        """
        @_wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
