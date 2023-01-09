#!/usr/bin/env python
"""case without samples"""
import os
from typing import TypeAlias
from itertools import groupby

Url: TypeAlias = str
UrlList: TypeAlias = list[Url]
FirstDomain: TypeAlias = str
urls_groupedby_first_domain: TypeAlias = dict[FirstDomain, UrlList]
# final structure (list of urls grouped by first domain)
GroupedUrls: TypeAlias = list[urls_groupedby_first_domain]


def key(url: Url) -> FirstDomain:
    return url.split('.')[-1]


def final_data(urls: UrlList) -> GroupedUrls:
    return [{domain: list(_urls)} for domain, _urls in groupby(sorted(urls, key=key), key=key)]


def main(block_sites: UrlList) -> GroupedUrls:
    """Handle samples. (API)"""
    return final_data(urls=block_sites)


if __name__ == '__main__':
    def read(file='data/roscomsvoboda/repl_1_raw_data.tmp') -> UrlList:
        directory = os.getenv('PROJECT_DIR', '../../../')
        with open(f'{directory}{file}') as fh:
            # (r := fh.read()) and r[0] == '[' and r[-1] == ']' and eval(r)
            return eval(fh.read())

    result = final_data(urls=read())
    print(result)
