from types import SimpleNamespace as _namespace

from parsers.constants import Constant as _base

_URL = URL = 'https://youtube.com'

# Directory for storing final data
PARSED_DIR = F'{_base.DIR.PARSED_DATA}youtube'
# File to store samples for extracting raw data
SAMPLE_FILE = F'{_base.DIR.USER_PARSERS}youtube/samples.txt'

PRINT_TO_STDOUT = True

# Checked by `curl`=======================================
# The block of code below has been automatically generated
# Delete condition or reasign `URL`
if 301 not in range(200, 400):
    URL = _base.URL.HTTPBIN_ORG
# ========================================================

PARAMS = '/playlist?list='

# who(1st, 2nd name)_about_nvidoes
AK_PYTHON_12 = 'PLlb7e2G7aSpQhNphPSpcO4daaRPeVstku'
DK_LINUX_12 = 'PLHHm04DXWzeKZycf_ZuBgxWdVBnrjE_mj'
DK_BASICS_12 = 'PLHHm04DXWzeKuhdGFHSEWDpdgoYpjPptR'
AS_NETWORKS_56 = 'PLtPJ9lKvJ4oiNMvYbOzCmWy6cRzYAh9B1'
# PLAYLIST_ID = AK_PYTHON_12
# PLAYLIST_ID = DK_LINUX_12
# PLAYLIST_ID = DK_BASICS_12
PLAYLIST_ID = AS_NETWORKS_56

constant_locals = _namespace(
    base=_base,
    URL=URL + PARAMS + PLAYLIST_ID,
    PARSED_DIR=PARSED_DIR,
    PRINT_TO_STDOUT=PRINT_TO_STDOUT,
    SAMPLE_FILE=SAMPLE_FILE,
    PLAYLIST_ID=PLAYLIST_ID
)
