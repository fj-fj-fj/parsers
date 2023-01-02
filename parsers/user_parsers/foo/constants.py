from types import SimpleNamespace as _namespce

from parsers.constants import Constant as _base

_URL = URL = 'https://foo.com'

# Directory for storing final data
PARSED_DIR = F'{_base.DIR.PARSED_DATA}foo'
# File to store samples for extracting raw data
SAMPLE_FILE = F'{_base.DIR.USER_PARSERS}foo/samples.txt'

PRINT_TO_STDOUT = True

# Checked by `curl`=======================================
# The block of code below has been automatically generated
# Delete condition or reasign `URL`
if 000 not in range(200, 400):
    URL = _base.URL.HTTPBIN_ORG
# ========================================================

constant_locals = _namespce(
    base=_base,
    URL=URL,
    PARSED_DIR=PARSED_DIR,
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    SAMPLE_FILE=SAMPLE_FILE,
)
