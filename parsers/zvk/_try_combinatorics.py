import itertools

url = (
    'https://zvk.ru/catalog/orgtekhnika/kopiry-mfu/filter/obem_pamyati-is-'
    '1024-or-1260-or-128-or-1280-or-131072-or-1512-or-1536-or-16-or-2048-or-256'
    '-or-2560-or-2867-or-3000-or-3072-or-32-or-3584-or-4096-or-4608-or-512-or-5120'
    '-or-5632-or-6-or-6144-or-64-or-768-or-8192-or-'
    '%D0%BD%D0%B5%D1%82-or-%D0%BD%D0%B5%D1%82%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85/'
)


def _combine_unique_params(url):
    base, parts = url.split('-is-')
    pool = parts[:-1].split('-or-')
    return (len(pool), base, pool)


def combine_unique_params(base, pool):
    length_subsequences = itertools.count(1)

    iteration = next(length_subsequences)
    while iteration < len(pool) + 1:
        for item in itertools.combinations(pool, iteration):
            params = '-or-'.join(item).removesuffix('-or-')
            yield f"{base}{'-is-' if iteration != 1 else '-'}{params}/\n"
        iteration = next(length_subsequences)


length_pool, base, pool = _combine_unique_params(url)

iterator = (i for i in combine_unique_params(base, pool))


with open('foo.tmp', 'a') as f:
    for _ in range(2 ** length_pool - 1):
        for i in itertools.islice(iterator, 100000):
            f.write(i)


# Try func() -> list[str]
# `list.append` works if `lenght_pool` <= 21 else killed

# Try func() -> Iteratror[str]
# green screen of death
#
#  .venv 3.10.0 ➜  wc -l foo.tmp
# 56643565 foo.tmp
#
#  .venv 3.10.0 ➜  du -sh foo.tmp
# 9.1G    foo.tmp
#
#  .venv 3.10.0 ➜  cat foo.tmp | tail -1
# https://zvk.ru/catalog/orgtekhnika/kopiry-mfu/filter/obem_pamyati-is-10


import os

os.makedirs('data', exist_ok=True)

def generate__268_435_455_files__by__100_000_lines():
    for number in range(2 ** length_pool - 1):
        with open(f'data/{number}_foo.tmp', 'a') as f:
            f.writelines(itertools.islice(iterator, 100000))

# i hesistate to run it
