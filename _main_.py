from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from scrapping import scrapping


def setup_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)


def main():
    driver = setup_driver()
    url = "https://news.yahoo.com/"
    scrapping(driver, url)
    time.sleep(200)
    driver.quit()


main()
