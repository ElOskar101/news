from selenium import webdriver
import time

from scrapping import scrapping


def setup_driver():
    options = webdriver.FirefoxOptions()
    return webdriver.Firefox(options=options)


def main():
    driver = setup_driver()
    url = "https://apnews.com/"
    scrapping(driver, url)
    time.sleep(200)
    driver.quit()


# TODO:
# Accept cookies
# Validate elements were not found
main()
