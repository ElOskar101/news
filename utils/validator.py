from utils.logging import Logger


class Validator:
    def __init__(self):
        self.logger = Logger().get_logger()
        pass

    def elm_exists(self, driver, selector, timeout):
        """
        This functions validates if an element exists.
        :param driver: selenium webdriver
        :param selector: Which element to check
        :param timeout: The limit time to check the element existence
        :return: Boolean: True if the element exists, False otherwise
        """
        try:
            driver.wait_until_element_is_visible(selector, timeout)
            return True
        except Exception as e:
            self.logger.warning(f"Error while getting element {selector}: {e}")
            return False

    def get_text(self, driver, selector, parent):
        """
        This function gets the text of an element but only if the element exists.
        :param driver: webdriver instance
        :param selector: The element to check
        :param parent: The parent locator for the selector
        :return: String: The text of the element or empty string if the element does not exist
        """
        try:
            element = driver.find_element(selector, parent)
            text = driver.get_text(element) if element else "None"
            return text
        except Exception as e:
            self.logger.warning(f"Error while getting element {selector}: {e}")
            return ''
