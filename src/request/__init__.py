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
    from inspect import signature
    from types import FunctionType

    print('[!] This module contains:\n')
    for obj in locals().copy().values():
        if isinstance(obj, FunctionType) and obj != signature:
            func_signature = f'def {obj.__name__}{signature(obj)}:\n'
            func_docstring = f'\t"""{obj.__doc__}"""\n'
            print(func_signature, func_docstring)

    print('[*] Shortcuts:')
    for func in exec, print:
        func('ch = check; chp = check_proxies; p = parse; pp = parse_proxies')  # type: ignore [operator]
