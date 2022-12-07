"""# TODO: clean up \U0001F4A9 and write docsting"""
from parsers.constants import Constant as _Constant

URL = 'https://test_template.com'  # FIXME: if needed      <---

# Checked by curl
__HTTP_STATUS_CODE = 000
# The server returns __HTTP_STATUS_CODE.
# The block of code below has been automatically generated
# for the convenience of the first parsing steps.
# Delete this block or reasign `URL` if needed.
if __HTTP_STATUS_CODE < 400:
    URL = _Constant.URL.HTTPBIN_ORG

PARSED_DIR = f'{_Constant.DIR.PARSED_DATA}test_template'
