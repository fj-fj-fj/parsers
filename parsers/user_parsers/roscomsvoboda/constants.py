from types import SimpleNamespace as _namespce

from parsers.constants import Constant as _base

_URL = URL = 'https://roscomsvoboda.com'

# Directory for storing final data
PARSED_DIR = F'{_base.DIR.PARSED_DATA}roscomsvoboda'
# File to store samples for extracting raw data
SAMPLE_FILE = F'{_base.DIR.USER_PARSERS}roscomsvoboda/samples.txt'

PRINT_TO_STDOUT = True

# Checked by `curl`=======================================
# The block of code below has been automatically generated
# Delete condition or reasign `URL`
if 000 not in range(200, 400):
    URL = _base.URL.HTTPBIN_ORG
# ========================================================

constant_locals = _namespce(
    base=_base,
    # The list of blocked domains
    URL='https://reestr.rublacklist.net/api/v3/ct-domains/',
    # The list of domains blocked through DPI
    URL_EXTRA=['https://reestr.rublacklist.net/api/v3/dpi/'],
    PARSED_DIR=PARSED_DIR,
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    SAMPLE_FILE=SAMPLE_FILE,
)
