while True:
    try:
        from request.proxy.checker import check
        from request.proxy.checker import check_proxies
        from request.proxy.parser import parse
        from request.proxy.parser import parse_proxies
        break
    except ModuleNotFoundError:
        __import__('patch').update_syspath(__file__)


if __name__ == '__main__':
    from types import FunctionType

    print('This module contains:')
    for obj in locals().copy().values():
        if isinstance(obj, FunctionType):
            print(f' {obj.__name__}()'.ljust(20) + f'- {obj.__doc__}')
