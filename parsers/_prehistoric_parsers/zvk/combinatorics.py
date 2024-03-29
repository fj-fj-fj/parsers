r"""
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
            _get_params(_split())
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


def _combine(elements, returned_len_subsequences = 2, _internal = True):
    # (list[str], int, bool) -> list[str] | list[Optional[tuple[str]]]
    if not _internal:
        # `_combine()` was called in other module,
        # save `returned_len_subsequences` as second parameter for `itertools.combinations`
        _combine.__len = returned_len_subsequences
    # get `_combine.__len` if saved, default otherwise
    len_subsequences = getattr(_combine, '__len', returned_len_subsequences)
    len_sec = itertools.count(len_subsequences)  # type: ignore

    combinations = []
    pool: list[str] = elements

    iteration = next(len_sec)
    while iteration <= len_subsequences:
        for params in itertools.combinations(pool, len_subsequences):  # type: ignore
            if len(set([el.split('is')[0] for el in params])) < len(params):
                continue
            # _internal = False if `_combine()` exports in other module
            comb_item = f''.join(params) if _internal else params
            combinations += [comb_item]
        iteration += 1

    return combinations


def _generate_combinations(urls):
    # (list[str | None] | list[tuple[str] | None]) -> list[str]
    formed_get_params = _decompose(urls)
    return _combine(formed_get_params)


def generate(urls: list[str]) -> list[str]:
    base_url = urls[0].rsplit('/', 2)[0]
    return [f'{base_url}/{params}\n' for params in _generate_combinations(urls)]


if __name__ == '__main__':
#region Test
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
#endregion Test
