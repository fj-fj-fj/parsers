import logging
from types import SimpleNamespace

from requests.structures import CaseInsensitiveDict

# base
CaseInsensitiveDictType = CaseInsensitiveDict[str]

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.WARNING)

HEADERS: CaseInsensitiveDictType = CaseInsensitiveDict({
    'Accept': '*/*',
    'Accept-Lanquage': 'ru',
    # 'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/84.0.4147.135 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
})

PARSED_DATA_DIRECTORY = 'parsed_data'

# гибдд.рф
GIBDD_URL = 'https://xn--90adear.xn--p1ai/r/65/news/region?'

GIBDD_PARAMS = {
    'region': 65,
    'perPage': 110,
    'page': 1,
}

GIBDD_FILES = SimpleNamespace(
    CSV='parsed_data/region_65_news.csv',  # unused
    CSV_HEADER=(  # unused
        'ID',
        'Title',
        'Description',
        'Author',
        'Region_code',
        'Region_name',
    ),
    TXT='parsed_data/posts_id.txt',
    JSON='parsed_data/{}_article.json',
)

GIBDD_CONFIG = SimpleNamespace(
    URL=GIBDD_URL,
    PARAMS=GIBDD_PARAMS,
    FILES=GIBDD_FILES,
)

# export
CONFIGURATION = GIBDD_CONFIG
CONFIGURATION.HEADERS = HEADERS
CONFIGURATION.DIR = PARSED_DATA_DIRECTORY
