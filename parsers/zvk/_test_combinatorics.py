import itertools


def _split(url: str) -> tuple[str, list[str]]:
    url_with_property_name, others = url.split('-is-')
    property_name = url_with_property_name.rsplit('/', 1)[-1]
    property_types = others[:-1].split('-or-')
    return (property_name, property_types)


def _decompose(urls: list[str]) -> list[tuple[str, list[str]]]:
    return [_split(url) for url in urls]


def _combine(items_by_propery_name, start = 2, stop = 2):
    # (list[tuple[str, list[str]]], int, int) -> list[str]
    params_combinations: list[str] = []
    pool: list[str] = []
    category, category_2 = items_by_propery_name
    len_sec = itertools.count(start)

    property_name, items = category
    for item in items:
        pool += [f'{property_name}-is-{item}/']

        property_name_2, items_2 = category_2
        for item_2 in items_2:
            pool += [f'{property_name_2}-is-{item_2}/']

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
    property_types_by_name = _decompose(urls)
    return _combine(property_types_by_name)


def generate(urls: list[str]) -> list[str]:
    base_url = urls[0].rsplit('/', 2)[0]
    return [f'{base_url}/{params}\n' for params in _generate_combinations(urls)]


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

assert 'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-brother/tsvetnost_pechati-is-tsvetnoy/\n' in results
assert 'https://zvk.ru/catalog/orgtekhnika/printery/filter/brand-is-brother/tsvetnost_pechati-is-cherno_belyy/\n' in results
assert results.__len__() == 2
