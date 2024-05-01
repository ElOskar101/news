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
        self.values = []
        self.logger = Logger().get_logger()
        utils = Utils()
        keys = utils.get_work_items()
        self.limit = keys['months']
        self.key = keys['search_phrase']
        self.news_category = keys['category']
        self.last_required_month = True  # Flag for previous months limit.
        self.driver = Selenium()

    # Close browser
    def close(self):
        self.driver.close_browser()

    # Open browser
    def open(self):
        driver = self.driver
        self.logger.info('Open browser')
        url = "https://apnews.com/"
        driver.open_available_browser(url, browser_selection='chrome')

    # Scraping through apnews.com
    def scrape(self):
        driver = self.driver
        v = Validator()
        self.open()  # Open browser
        self.search_news()  # Search logic

        self.logger.info('Loop starting for news articles pagination')
        while self.last_required_month:  # Loop through the pages until there are no more news in the given range
            if not v.validate(driver, 'css:div.PageList-items', 10):
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

    # Search news articles
    def search_news(self):
        driver = self.driver
        v = Validator()
        v.validate(driver, 'css:.Page-header-bar', 10)

        driver.click_element_if_visible("//*[contains(text(),  'I Accept')]")
        if not v.validate(driver, 'css:button.SearchOverlay-search-button', 10):
            driver.click_element_if_visible('css:.bx-close.bx-close-link.bx-close-inside')

        driver.click_element_if_visible('css:button.SearchOverlay-search-button')
        if not v.validate(driver, 'css:input.SearchOverlay-search-input', 10):
            return False
        search_box = driver.find_element('css:input.SearchOverlay-search-input')
        if search_box:
            driver.input_text(search_box, self.key)
            driver.press_keys(search_box, 'ENTER')
        self.logger.info('Searching for: ' + self.key)
        if not v.validate(driver, 'css:div.PageList-items', 10):
            return False
        if not v.validate(driver, 'css:select.Select-input', 10):
            return False

        driver.select_from_list_by_index('css:select.Select-input', '1')
        self.logger.info('Selecting sort')
        time.sleep(2)  # Not immediately reaction and the next wait would be already loaded meaning a false true
        if not v.validate(driver, 'css:div.PageList-items', 10):
            return False

        driver.click_element('css:div.SearchFilter-heading')
        categories_section = driver.find_elements('css:ul.SearchFilter-items > li')
        self.logger.info('Selecting category')
        for category in categories_section:  # Select a category
            section_text = v.get_text(driver, 'css:span', category)
            if section_text.lower().strip() == self.news_category:
                driver.click_element(driver.find_element('css:input[type="checkbox"]', category))
                self.logger.info('Selecting news category')
                time.sleep(2)  # Not immediately reaction and the next wait would be already loaded meaning a false true
                break
            else:
                self.logger.warning('No categories were found: %s', section_text)

    # Loop news articles
    def get_news(self, articles):
        driver = self.driver
        v = Validator()
        utils = Utils()
        for i in range(len(articles)):  # Loop through the articles extracting all the news information requested
            promo_content = driver.find_element('css:.PagePromo > .PagePromo-content', articles[i])
            title = v.get_text(driver, 'css:div.PagePromo-title > a > span', promo_content)
            desc = v.get_text(driver, 'css:.PagePromo-description', promo_content)
            date = v.get_text(driver, 'css:.PagePromo-byline', promo_content)
            phrase_count = (utils.count_phrase_occurrences(title, self.key)
                            + utils.count_phrase_occurrences(desc, self.key))
            does_it_have_currency_format = (utils.validate_currency_format(title)
                                            or utils.validate_currency_format(desc))
            name = ''

            try:
                image = driver.find_element('css:img', articles[i])
                if image:
                    name = f"output/image-{utils.generate_file_name()}.png"
                    driver.screenshot(image, name)
                    time.sleep(1)
            except Exception as e:
                self.logger.error('Exception occurred: %s', e)

            self.values.append([title, desc, date.replace('Updated ', ''),
                                phrase_count, does_it_have_currency_format, os.path.basename(name)])
            self.last_required_month = utils.validate_news_date_range(date, self.limit)
            if not self.last_required_month:
                break

    # It sends needed information in order to save it in a .xlsx file
    def insert_data(self, data: list):
        self.logger.info('Inserting rows in Excel file')
        filer = Filer()
        filer.create_excel()
        filer.insert_data(data=data, start_col=1, start_row=1)
        filer.save()
        self.logger.info('Excel file saved')
