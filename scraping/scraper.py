from RPA.Browser.Selenium import Selenium
from utils.validator import Validator
from utils.logging import Logger
from scraping.filer import Filer
from utils.utils import Utils
import time
import os


# Makes all the scraping logic and information treatment after extraction
class Scrapper:
    def __init__(self):
        """Init shared variables or functions"""
        self.values = []
        self.logger = Logger().get_logger()
        self.elm_validator = Validator()
        self.utils = Utils()
        keys = self.utils.get_work_items()
        self.limit = keys['months']
        self.start_date, self.end_date = self.utils.calculate_dates(self.limit)
        self.key = keys['search_phrase']
        self.news_category = keys['category']
        self.last_required_month = True  # Flag for previous months limit.
        self.DEFAULT_TIMEOUT = 5
        self.driver = Selenium()

    def close(self):
        """Close browser"""
        self.driver.close_browser()

    def open(self):
        """Open browser"""
        driver = self.driver
        self.logger.info('Open browser')
        URL = "https://apnews.com/"
        driver.open_available_browser(URL, browser_selection='chrome')

    def scrape(self):
        """Orchestrate scraping. It searches news by given criteria and iterate articles"""
        driver = self.driver
        self.open()  # Open browser
        self.search_news()  # Search logic

        self.logger.info('Loop starting for news articles pagination')
        while self.last_required_month:  # Loop through the pages until there are no more news in the given range
            if not self.elm_validator.elm_exists(driver, 'css:div.PageList-items', self.DEFAULT_TIMEOUT):
                continue

            content = driver.find_element('css:div.PageList-items')
            articles = driver.find_elements('css:div.PageList-items-item', content)
            articles.pop(0)  # always first new is sponsored news, or it could be out of range

            self.get_news(articles)  # loop news method

            if self.last_required_month:
                driver.click_element('css:.Pagination-nextPage')
            else:
                self.logger.info('No more news available in this range. End of process')

        self.insert_data(self.values)

    def search_news(self):
        """Search news articles by a given phrase called 'key'"""
        driver = self.driver
        self.elm_validator.elm_exists(driver, 'css:.Page-header-bar', self.DEFAULT_TIMEOUT)

        driver.click_element_if_visible("//*[contains(text(),  'I Accept')]")
        if not self.elm_validator.elm_exists(driver, 'css:button.SearchOverlay-search-button', self.DEFAULT_TIMEOUT):
            driver.click_element_if_visible('css:.bx-close.bx-close-link.bx-close-inside')

        driver.click_element_if_visible('css:button.SearchOverlay-search-button')
        if not self.elm_validator.elm_exists(driver, 'css:input.SearchOverlay-search-input', self.DEFAULT_TIMEOUT):
            return False
        search_box = driver.find_element('css:input.SearchOverlay-search-input')
        if search_box:
            driver.input_text(search_box, self.key)
            driver.press_keys(search_box, 'ENTER')
        self.logger.info('Searching for: ' + self.key)
        if not self.elm_validator.elm_exists(driver, 'css:div.PageList-items', self.DEFAULT_TIMEOUT):
            return False
        if not self.elm_validator.elm_exists(driver, 'css:select.Select-input', self.DEFAULT_TIMEOUT):
            return False

        driver.select_from_list_by_index('css:select.Select-input', '1')
        self.logger.info('Selecting sort')
        time.sleep(2)  # Not immediately reaction and the next wait would be already loaded meaning a false true
        if not self.elm_validator.elm_exists(driver, 'css:div.PageList-items', self.DEFAULT_TIMEOUT):
            return False

        driver.click_element('css:div.SearchFilter-heading')
        categories_section = driver.find_elements('css:ul.SearchFilter-items > li')
        self.logger.info('Selecting category')
        for category in categories_section:  # Select a category
            section_text = self.elm_validator.get_text(driver, 'css:span', category)
            if section_text.lower().strip() == self.news_category:
                driver.click_element(driver.find_element('css:input[type="checkbox"]', category))
                self.logger.info('Selecting news category')
                time.sleep(2)  # Not immediately reaction and the next wait would be already loaded meaning a false true
                break
            else:
                self.logger.warning('No categories were found: %s', section_text)

    def get_news(self, articles):
        """Scrape each article and validate information according to steps"""
        driver = self.driver

        for i in range(len(articles)):  # Loop through the articles extracting all the news information requested
            promo_content = driver.find_element('css:.PagePromo > .PagePromo-content', articles[i])
            date = self.elm_validator.get_text(driver, 'css:.PagePromo-byline', promo_content)

            if not self.utils.validate_news_date_range(date, self.start_date, self.end_date):
                self.last_required_month = False
                break

            title = self.elm_validator.get_text(driver, 'css:div.PagePromo-title > a > span', promo_content)
            desc = self.elm_validator.get_text(driver, 'css:.PagePromo-description', promo_content)
            phrase_count = (self.utils.count_phrase_occurrences(title, self.key)
                            + self.utils.count_phrase_occurrences(desc, self.key))
            does_it_have_currency_format = (self.utils.validate_currency_format(title)
                                            or self.utils.validate_currency_format(desc))
            name = ''

            try:
                image = driver.find_element('css:img', articles[i])
                if image:
                    name = f"output/image-{self.utils.generate_file_name()}.png"
                    driver.screenshot(image, name)
            except Exception as e:
                self.logger.error('Exception occurred: %s', e)

            self.values.append([title, desc, date.replace('Updated ', ''),
                                phrase_count, does_it_have_currency_format, os.path.basename(name)])

    def insert_data(self, data: list):
        """It sends needed information in order to save it in a .xlsx file"""
        self.logger.info('Inserting rows in Excel file')
        filer = Filer()
        filer.create_excel()
        filer.insert_data(data=data, start_col=1, start_row=1)
        filer.save()
        self.logger.info('Excel file saved')
