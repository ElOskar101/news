from selenium import webdriver
from RPA.Browser.Selenium import Selenium
import time


def setup_driver():
    return Selenium()

def main():
    driver = setup_driver()
    url = "https://apnews.com/"
    scrapping(driver, url)
    time.sleep(200)
    # driver.quit()




# TODO:
# Accept cookies
# Validate elements were not found
main()

"""


work_items = WorkItems()
work_items.get_input_work_item()
work_item = work_items.get_work_item_variables()

{
    "key":"value"
}
"""
