from RPA.Browser.Selenium import Selenium
from utils.logging import Logger


class Validator:
    def __init__(self):
        logger = Logger()
        self.logging = logger.get_logger()
        pass

    # Validate that element exists
    def validate(self, driver, selector, timeout):
        try:
            driver.wait_until_element_is_visible(selector, timeout)
            return True
        except Exception as e:
            print(f"Error while getting element {selector}: {e}")
            self.logging.critical('Element not found')
            return False

    # Get text of an element than cannot exists
    def get_text(self, driver, selector, parent):
        try:
            element = driver.find_element(selector, parent)
            text = driver.get_text(element) if element else "None"
            return text
        except Exception as e:
            print(f"Error while getting element {selector}: {e}")
            self.logging.critical(f'No text found {e}')
            return ''
