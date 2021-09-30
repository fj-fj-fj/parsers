from pathlib import Path
from typing import Generator

import combinatorics

PATH = Path('parsers/zvk/data')

ALL_PARSED_FILE = '_all_parsed_{}'

EXCLUDE_FILES = {
    '_all_parsed',
}

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
    # (Path, set[str]) -> dict[str, dict[str, set[str]]] | None
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
        if all([
            p.is_file(),
            not p.match('*_[0-9]'),
            p.name not in EXCLUDE_FILES,
        ]):
            yield read(p)


def make_long_url(category: str, parts: set[str]) -> str:
    base_url, *others = (s for p in parts for s in p.rsplit('/', 2))
    _parts = {item for item in others if item and item != base_url}
    url_params = {i for p in _parts for i in p.split('-') if i != category}
    return f"{base_url}/{category}-is-{'-or-'.join(url_params)}/"


def save(
    file: Path,
    data: list[str],
    mode: str = 'a',
    prefix_file: int = 1,
    common_file = ALL_PARSED_FILE,
):
    # save into local files
    file_name = f'{file.name}_{prefix_file}'
    file_path = file.parent/file_name
    with file_path.open(mode) as f:
        f.writelines(data)

    # save into common file
    all_parsed_name = common_file.format(prefix_file)
    file_path = file.parent.parent/all_parsed_name
    with file_path.open(mode) as f:
        f.writelines(data)


def generate_multiple_params_urls(count_urls: int):
    for categories_by_file in readfiles():
        if categories_by_file is not None:
            for file, categories in categories_by_file.items():
                print(f'{file=}')

                long_urls = []
                for stem, value in categories.items():
                    url = make_long_url(stem, value)
                    print(f'\t{stem=},\n\t\t{url=}')
                    long_urls += [url]

                combinations = combinatorics._combine(
                    elements=long_urls,
                    returned_len_subsequences=count_urls,
                    _internal=False,
                )
                for combination in combinations:
                    result = combinatorics.generate(combination)
                    save(Path(file), result, prefix_file=count_urls)


def main(**count_urls):
    generate_multiple_params_urls(**count_urls)


if __name__ == '__main__':
    main(count_urls=2)
    main(count_urls=3)
    main(count_urls=4)
