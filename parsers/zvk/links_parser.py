import logging
import os
from contextlib import suppress
from time import sleep
from typing import Optional

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException as E1,
    ElementNotInteractableException as E2,
    NoSuchElementException as E3,
)
from selenium.webdriver.remote.webelement import (
    WebElement,
    WebDriverException,
)
from urllib3.exceptions import MaxRetryError

from driver import chrome

# paths system
PARSED_DATA_DIR = f'{os.getcwd()}/parsers/zvk/data/'
PARSED_DATA_FILE = '_parsed_data_default'
ALL_PARSED_FILE = '_all_parsed'

# paths source
_base_url = 'https://zvk.ru'
_orgtekhnika = f'{_base_url}/catalog/orgtekhnika'
URL = f'{_orgtekhnika}/printery-etiketok/'

del _base_url, _orgtekhnika

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ZVK')
for name in ('urllib3', 'selenium'):
    logging.getLogger(name).setLevel(level=logging.WARNING)


useragent = UserAgent()


options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.chrome}')
options.add_argument('--start-maximized')


def initialyze_driver() -> webdriver.Chrome:
    return webdriver.Chrome(
        executable_path=chrome.driver,
        service_log_path=chrome.log_file,
        options=options,
    )


def close(driver: Optional[webdriver.Chrome]):
    driver and driver.quit()


def set_file_name(url: str):
    global PARSED_DATA_FILE
    PARSED_DATA_FILE = os.path.basename(os.path.normpath(url))


def _wait_database_response(seconds: float = 6):
    sleep(seconds)


def _smooth_click(element: WebElement):
    sleep(.3); element.click()


def slider_exists_in(category: WebElement) -> bool:
    slider_element = ".//a[contains(@id, 'left_slider')]"
    return bool(category.find_elements_by_xpath(slider_element))


def show_all_elements_in(category: WebElement):
    pattern = './/button[@class="ash1133__new__filter__show__other"]'
    with suppress(E3):
        button = category.find_element_by_xpath(pattern)
        _is_button_with_hide_text(button) or _smooth_click(button)


def _is_button_with_hide_text(button: str) -> bool:
    return getattr(button, 'text') != 'Показать все значения'


def fetch_url_with_all_elements_in(category: WebElement, sec: float = 3) -> str:
    _click_all_elements_in(category, 'select')
    pattern = '..//div[@class="bx-filter-popup-result left"]/a'
    with suppress(E3):
        a = category.find_element_by_xpath(pattern).get_attribute('href')
    sleep(sec)
    _click_all_elements_in(category, 'unselect')
    return a  # type: ignore


def _click_all_elements_in(category: WebElement, action: str):
    pattern = '..//div[@class="bx-filter-parameters-box-title"]'
    title = category.find_element_by_xpath(pattern)
    logging.debug(f"'{title.text}': {action} all elements...")
    for label in category.find_elements_by_xpath('div//label'):
        with suppress(E1, E2):
            _smooth_click(label)
    _wait_database_response()


def make_links(row_url: str) -> list[str]:
    logging.debug(f'{row_url=}\n')  # insert `\n` before new `iteration`
    url, params = row_url.split('is-')
    return [_construct_(url, element) for element in params.split('-or-')]


def _construct_(url: str, params: str) -> str:
    return ''.join(f"{url}{params}{'' if '/' in params else '/'}\n")


def save_to(
    file_cur_data: str,
    data: list[str],
    file_cur_data_loc: str = PARSED_DATA_DIR,
    file_all_data: str = ALL_PARSED_FILE,
    file_all_data_loc: str = PARSED_DATA_DIR,
):
    os.makedirs(file_cur_data_loc, exist_ok=True)
    os.makedirs(file_all_data_loc, exist_ok=True)

    with (
        open(file_cur_data_loc + file_cur_data, 'a') as f_local,
        open(file_all_data_loc + file_all_data, 'a+') as f_common,
    ):
        with suppress(TypeError):  # skip if NoneType
            f_local.writelines(data)

            with suppress(ValueError):  # negative seek position -1
                # step back if the line is empty
                if not (f := f_common).read(1):
                    f.seek(f.tell() - 1, os.SEEK_SET)

            f_common.writelines(data)

        logging.debug(f'data into {f_local.name} saved.')
        logging.debug(f'data into {f_common.name} added.\n')


def _parse(driver: webdriver.Chrome):
    set_file_name(driver.current_url)

    current_iteration = 1  # skip 0th category with slider
    while current_iteration < len((categories := driver.find_elements_by_class_name('bx-filter-block'))):
        category = categories[current_iteration]
        logging.debug(f"{category.text.replace(f'{chr(10)}', '-')}")

        if not category.text:
            break  # e.g., last category is empty

        if slider_exists_in(category):
            current_iteration += 1
            continue

        show_all_elements_in(category)
        fetched = fetch_url_with_all_elements_in(category)
        urls = make_links(row_url=fetched)
        save_to(PARSED_DATA_FILE, urls)
        current_iteration += 1


def main(driver: webdriver.Chrome):
    _parse(driver)
    logging.debug(' * Done! *')


from config.REPL.helpers import *

set_interactive_mode()
register_python_history_file()

try:
    driver: Optional[webdriver.Chrome] = initialyze_driver()
except WebDriverException as e:
    XLAUNCH_AS_POSSIBLE_PROBLEM = f'{e!r}\vCheck `XLaunch` health!\v'
else:
    try:
        driver.get(url=URL)
    except MaxRetryError as failed_new_connection:
        logging.exception(failed_new_connection)
    try:
        main(driver)
    except Exception as unknoun_shit:
        logging.exception(unknoun_shit)
finally:
    try:
        os.environ.get('PYTHONINSPECT', close(driver))  # type: ignore
    except NameError:
        logging.exception(XLAUNCH_AS_POSSIBLE_PROBLEM)  # type: ignore
