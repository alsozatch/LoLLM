from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def scroll_page_down(query_url, pagedown_count=10):
    """
    Scrolls the query_url page down the specified number of times.

    Assumes the body tag is scrollable & interactable.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(query_url)

    elem = driver.find_element(By.XPATH, '//body')

    while pagedown_count > 0:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        pagedown_count-=1

    return driver.page_source