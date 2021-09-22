#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#region Imports
import logging
import os
from contextlib import suppress
from time import sleep
from typing import Iterator

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
#endregion Imports

#region Variables

#region Constants
BASE_URL = 'https://zvk.ru'
BASE_PARSED_DATA_DIR = f'{os.getcwd()}/parsers/zvk/data/'
ALL_PARSED_FILE = '_all_parsed'
#endregion Constants


current_parsed_dir = 'dynamically_assigned_name_of_current_category'
parsed_data_file = 'dynamically_assigned_name_of_current_subcategory'

categories_names: Iterator[str] | None
#endregion Variables


#region Configurations
FORMAT = "%(filename)s:%(lineno)s::%(funcName)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

for name in ('urllib3', 'selenium'):
    logging.getLogger(name).setLevel(level=logging.WARNING)


options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={UserAgent().chrome}')
options.add_argument('--start-maximized')
#endregion Configurations


#region Functions

#region Utils
def set_file_name(url: str):
    global parsed_data_file
    parsed_data_file = os.path.basename(os.path.normpath(url))


def set_directory(name: str):
    global current_parsed_dir
    current_parsed_dir = f'{BASE_PARSED_DATA_DIR}{name}/'


def make_dirs(names: list[str]):
    global categories_names
    categories_names = iter(names)
    for name in names:
        os.makedirs(f'{BASE_PARSED_DATA_DIR}{name}/', exist_ok=True)
        logger.debug(f' - mkdir data/{name}/')


def make_links(row_url: str) -> list[str]:
    logger.debug(f' {row_url=}\n')  # insert `\n` before new `iteration`
    url, params = row_url.split('is-')
    return [_construct(url, element) for element in params.split('-or-')]


def _construct(url: str, params: str) -> str:
    return ''.join(f"{url}{params}{'' if '/' in params else '/'}\n")


def save_to(
    local_flle: str,
    data: list[str],
    common_flle: str = ALL_PARSED_FILE,
):
    current_parsed_data = f'{current_parsed_dir}{local_flle}'
    full_parsed_data = f'{BASE_PARSED_DATA_DIR}{common_flle}'
    with (
        open(current_parsed_data, 'a') as f_local,
        open(full_parsed_data, 'a+') as f_common,
    ):
        with suppress(TypeError):  # skip if NoneType
            f_local.writelines(data)

            with suppress(ValueError):  # negative seek position -1
                # step back if the line is empty
                if not (f := f_common).read(1):
                    f.seek(f.tell() - 1, os.SEEK_SET)

            f_common.writelines(data)

        logger.debug(f'\t - {f_local.name} saved -')
        logger.debug(f'\t - {f_common.name} added -\n')
#endregion Utils


#region Driver
def initialyze_driver() -> webdriver.Chrome:
    return webdriver.Chrome(
        executable_path=chrome.driver,
        service_log_path=chrome.log_file,
        options=options,
    )


def close(driver: webdriver.Chrome | None = None):
    driver is None or driver.quit()
#endregion Driver


#region Parser-Utils
def _smooth_click(element: WebElement):
    sleep(.3); element.click()


def _wait_database_response(seconds: float = 6):
    sleep(seconds)


def _cut_tail_from(links: list[WebElement]) -> list[str]:
    return [a.get_attribute('href').rsplit('/', 2)[1] for a in links]


def _is_button_with_hide_text(button: str) -> bool:
    return getattr(button, 'text') != 'Показать все значения'
#endregion Parser-Utils


#region Parser
def scrape_aside_panel(driver: webdriver.Chrome) -> dict[str, list[str]]:
    categories: list[WebElement] = _scrape_menu(driver)
    tails: list[str] = _cut_tail_from(categories)
    make_dirs(tails)

    urls_by_categories: dict[str, list[str]] = {}

    for category in categories:
        subcategories: list[WebElement] = _scrape_submenu(category)

        with suppress(StopIteration):
            category_name: str = next(categories_names)  # type: ignore
            hrefs: list[str] = [a.get_attribute('href') for a in subcategories]
            urls_by_categories[category_name] = hrefs

    return urls_by_categories


def _scrape_menu(driver: webdriver.Chrome) -> list[WebElement]:
    pattern = '//aside//a[@class="menu-list__title"]'
    return (d := driver.find_elements_by_xpath(pattern))[:int(len(d)/2)]
    # NOTE: Tag <a> contains 2 submenu and function returns x2 items


def _scrape_submenu(category: WebElement) -> list[WebElement]:
    pattern = '..//ul/*/*/a'
    return category.find_elements_by_xpath(pattern)


def slider_exists_in(category: WebElement) -> bool:
    slider_element = ".//a[contains(@id, 'left_slider')]"
    return bool(category.find_elements_by_xpath(slider_element))


def show_all_elements_in(category: WebElement):
    pattern = './/button[@class="ash1133__new__filter__show__other"]'
    with suppress(E3):
        button = category.find_element_by_xpath(pattern)
        _is_button_with_hide_text(button) or _smooth_click(button)


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
    logger.debug(f" '{title.text}': {action} all elements...")
    for label in category.find_elements_by_xpath('div//label'):
        with suppress(E1, E2):
            _smooth_click(label)
    _wait_database_response()


def _parse(driver: webdriver.Chrome):
    set_file_name(driver.current_url)

    current_iteration = 1  # skip 0th category with slider
    while current_iteration < len((
        categories := driver.find_elements_by_class_name('bx-filter-block')
    )):
        category = categories[current_iteration]
        logger.debug(f" {category.text.replace(f'{chr(10)}', '-')}")

        if not category.text:
            break  # e.g., last category is empty

        if slider_exists_in(category):
            current_iteration += 1
            continue  # skip all diapazons

        show_all_elements_in(category)
        fetched = fetch_url_with_all_elements_in(category)
        urls = make_links(row_url=fetched)
        save_to(parsed_data_file, urls)
        current_iteration += 1


def main(driver: webdriver.Chrome):
    for category, links in scrape_aside_panel(driver).items():
        logger.info(f'{category}:')
        set_directory(category)
        for url in links:
            logger.info(f'\t{url}')
            driver.get(url=url)
            try:
                _parse(driver)
            except Exception as E:
                print(repr(E))
        logger.info(f'\v - All urls in "{category}" parsed done! -\n')
    logger.info(' -*- ALL CATEGORIES PARSED DONE! -*-')
#endregion Parser
#endregion Functions

#region __main__
from config.REPL.helpers import *

register_python_history_file()

try:
    driver: webdriver.Chrome | None = initialyze_driver()
except WebDriverException as e:
    logger.exception(f'{e!r}\vCheck `XLaunch` health!\v')
else:
    try:
        driver.get(url=BASE_URL)
    except MaxRetryError as failed_new_connection:
        logger.exception(failed_new_connection)
    try:
        main(driver)
    except Exception as unknoun_shit:
        set_interactive_mode()
        logger.exception(f'{unknoun_shit=!r}')
finally:
    os.environ.get('PYTHONINSPECT') or close(driver)  # type: ignore
#endregion __main__
