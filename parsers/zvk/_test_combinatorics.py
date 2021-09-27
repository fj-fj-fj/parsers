r"""
This script combines all unique links with two parameters
from two other with multiple parameters links.

Example:
    >>> generate([ # doctest: +NORMALIZE_WHITESPACE
    ... 'http://site.com/ONE-is-foo-or-bar/',
    ... 'http://site.com/TWO-is-spam-or-egg/',
    ... ])
    ['http://site.com/ONE-is-foo/TWO-is-spam/\n', 'http://site.com/ONE-is-foo/TWO-is-egg/\n',
    'http://site.com/ONE-is-bar/TWO-is-spam/\n', 'http://site.com/ONE-is-bar/TWO-is-egg/\n']

generate()
    _generate_combinations()
        _decompose()
            _split()
            _get_params()
    _combine()
"""
import itertools


def _split(url: str) -> tuple[str, list[str]]:
    url_with_property_name, others = url.split('-is-')
    property_name = url_with_property_name.rsplit('/', 1)[-1]
    property_types = others[:-1].split('-or-')
    return (property_name, property_types)


def _get_params(decomposed_url: tuple[str, list[str]]) -> list[str]:
    property_name, items = decomposed_url
    return [f'{property_name}-is-{item}/' for item in items]


def _decompose(urls: list[str]) -> list[str]:
    return [p for pool in (_get_params(_split(u)) for u in urls) for p in pool]


def _combine(formed_get_params: list[str], start = 2, stop = 2) -> list[str]:
    params_combinations: list[str] = []
    pool: list[str] = formed_get_params
    len_sec = itertools.count(start)

    iteration = next(len_sec)
    while iteration <= stop:
        for param, param_2 in itertools.combinations(pool, start):
            property_name_param = param.split('is')[0]
            property_name_param_2 = param_2.split('is')[0]
            if property_name_param == property_name_param_2:
                continue
            params_combinations += [f'{param}{param_2}']
        iteration += 1

    return params_combinations


def _generate_combinations(urls: list[str]) -> list[str]:
    formed_get_params = _decompose(urls)
    return _combine(formed_get_params)


def generate(urls: list[str]) -> list[str]:
    base_url = urls[0].rsplit('/', 2)[0]
    return [f'{base_url}/{params}\n' for params in _generate_combinations(urls)]


if __name__ == '__main__':
    brand_url = (
        'https://zvk.ru/'
        'catalog/orgtekhnika/printery/'
        'filter/brand-is-'
        'brother'
        '-or-canon'
        '-or-epson'
        '-or-hp'
        '-or-konica-minolta'
        '-or-kyocera'
        '-or-lexmark'
        '-or-oki'
        '-or-pantum'
        '-or-ricoh'
        '-or-sharp'
        '-or-xerox/'
    )
    tsvetnost_pechati_url = (
        'https://zvk.ru/catalog/orgtekhnika/printery/'
        'filter/tsvetnost_pechati-is-'
        'tsvetnoy'
        '-or-cherno_belyy/'
    )

    results = generate(urls=[brand_url, tsvetnost_pechati_url])


    count = lambda url: len(url.split('-or-'))
    COUNT_BRANDS, COUNT_TSVETNOST_PECHATI = count(brand_url), count(tsvetnost_pechati_url)

    assert results.__len__() == COUNT_BRANDS * COUNT_TSVETNOST_PECHATI
    assert results == [
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-brother/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-brother/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-canon/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-canon/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-epson/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-epson/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-hp/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-hp/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-konica-minolta/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-konica-minolta/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-kyocera/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-kyocera/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-lexmark/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-lexmark/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-oki/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-oki/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-pantum/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-pantum/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-ricoh/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-ricoh/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-sharp/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-sharp/tsvetnost_pechati-is-cherno_belyy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-xerox/tsvetnost_pechati-is-tsvetnoy/\n',
        'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-xerox/tsvetnost_pechati-is-cherno_belyy/\n'
    ]
