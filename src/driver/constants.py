from os import getcwd as _pwd

CHROMEDRIVER_DIR = f'{_pwd()}/driver/chrome'
CHROMEDRIVER = f'{CHROMEDRIVER_DIR}/chromedriver'
CHROMEDRIVER_LOG_FILE = f'{CHROMEDRIVER_DIR}/.chromedriver.log'
