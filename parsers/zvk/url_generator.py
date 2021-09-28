from pathlib import Path
from typing import Generator

import combinatorics

PATH = Path('parsers/zvk/data')

needed_properties = {
    'brand',
    'proizviditel',
    'max_format',
    'tekhnologiya_pechati',
    'tsvetnost_pechati',
}


def walk(path: Path) -> Generator[Path, None, None]:
    for p in Path(path).iterdir():
        if p.is_dir():
            yield from walk(p)
            continue
        yield p.resolve()


def _stem(line: str, sep = 'filter/', idx = -1, sep2 = '-', idx2 = 0) -> str:
    return line.rpartition(sep)[idx].split(sep2)[idx2]


def read(file, stems = needed_properties):
    # (Path, set[str]) -> dict[str, str[str]] | None
    with open(file) as f:
        lines, fname =  f.readlines(), f.name #_stem(f.name, sep='zvk', sep2='None')

    urls = {fname: {s:set() for line in lines if (s := _stem(line)) in stems}}

    for line in lines:
        if (key := _stem(line)) in stems:
            urls[fname][key].add(line.strip())

    more_than_one_category = len(urls[fname]) > 1
    return urls if more_than_one_category else None


def readfiles(path = PATH):
    for p in walk(path):
        if p.is_file():
            yield read(p)


def make_long_url(category: str, parts: set[str]) -> str:
    base_url, *others = (s for p in parts for s in p.rsplit('/', 2))
    _parts = {item for item in others if item and item != base_url}
    url_params = {i for p in _parts for i in p.split('-') if i != category}
    return f"{base_url}/{category}-is-{'-or-'.join(url_params)}/"


def save(file, data: list[str], path: Path = PATH, mode='w'):
    filename = file.name
    path = file.parent
    filepath = path/f'{filename}_2'
    with filepath.open(mode) as f:
        f.writelines(data)


def generate_multiple_params_urls(count_urls):
    for categories_by_file in readfiles():
        if categories_by_file is not None:
            for file, categoties in categories_by_file.items():
                print(f'{file=}')
                generation_order = []
                for index, (stem, value) in enumerate(categoties.items(), 1):
                    url = make_long_url(stem, value)
                    print(f'\t{stem=},\n\t\t{url=}')
                    generation_order += [url]
                    if index == count_urls:
                        result = combinatorics.generate(generation_order)
                        save(Path(file), result)


def main(count_urls: int = 2):
    generate_multiple_params_urls(count_urls)


if __name__ == '__main__':
    main()
