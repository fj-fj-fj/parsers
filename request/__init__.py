while True:
    try:
        from proxy.parser import parse
        from proxy.parser import parse_proxies
        from proxy.checker import check
        break
    except ModuleNotFoundError:
        __import__('patch').update_syspath(__file__)


if __name__ == '__main__':
    from types import FunctionType

    print('This module contains:')
    for obj in locals().copy().values():
        if isinstance(obj, FunctionType):
            print(f' {obj.__name__}() - {obj.__doc__}')
