import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging


def scrapping(driver, url):
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "button.SearchOverlay-search-button").click()

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.SearchOverlay-search-input")))
    if search_box:
        time.sleep(2)
        search_box.send_keys("planes")
        search_box.send_keys(Keys.ENTER)
    else:
        print('Search box not found')
        return

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.SearchResultsModule-ajax')))

    relevance_filter_selector = Select(driver.find_element(By.CSS_SELECTOR, "select.Select-input"))
    relevance_filter_selector.select_by_index(1)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.SearchResultsModule-ajax')))
    time.sleep(3)

    content = driver.find_element(By.CSS_SELECTOR, '.SearchResultsModule-main')
    articles = content.find_elements(By.CSS_SELECTOR, ".PageList-items > .PageList-items-item")
    articles.pop(0)

    for i in range(len(articles)):
        promo_content = articles[i].find_element(By.CSS_SELECTOR, ".PagePromo > .PagePromo-content")

        title = promo_content.find_element(By.CSS_SELECTOR, "div.PagePromo-title > a > span").text
        description = promo_content.find_element(By.CSS_SELECTOR, ".PagePromo-description").text
        date = promo_content.find_element(By.CSS_SELECTOR, ".PagePromo-byline").text
        try:
            image = articles[i].find_element(By.CSS_SELECTOR, "img")
            if image and i < 5:
                image.screenshot(f"image{i}.png")
                time.sleep(1)
        except:
            print(f'Image not found')
    print('End of process')

        # print('~ '+title, '\n', '~ '+description,  '\n', '~ '+date, '\n\n')
    # driver.find_element(By.CSS_SELECTOR, 'button[value="Search"]').click()
