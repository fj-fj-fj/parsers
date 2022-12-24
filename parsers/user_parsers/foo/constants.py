"""# TODO: clean up \U0001F4A9 or be with it"""
from types import SimpleNamespace as _namespce

from parsers.constants import Constant as _base

_URL = URL = 'https://foo.com'  # FIXME: if needed      <<----

# Directory for storing data
PARSED_DIR = f'{_base.DIR.PARSED_DATA}foo'
# File to store sample strings (will be needed for `main()`)
SAMPLE_FILE = F'{_base.DIR.USER_PARSERS}foo/samples.txt'

PRINT_TO_STDOUT = True

# Checked by `curl`==============================
__HTTP_STATUS_CODE = 000  # FIXME: del           <<----
# The server returns __HTTP_STATUS_CODE.
# The block of code below has been automatically generated
# for the convenience of the first parsing steps.
# Delete this block or reasign `URL` if needed.
if __HTTP_STATUS_CODE < 400:
    URL = _base.URL.HTTPBIN_ORG
# ===============================================

# Export this namespace for all local parser constants
constant_locals = _namespce(
    base=_base,
    URL=URL,
    PARSED_DIR=PARSED_DIR,
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    SAMPLE_FILE=SAMPLE_FILE,
)

