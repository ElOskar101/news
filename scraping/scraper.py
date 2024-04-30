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
        utils = Utils()
        keys = utils.get_work_items()
        self.limit = keys['months']  # 1
        self.key = keys['search_phrase']  # 'planes'
        self.news_category = keys['category']  # 'stories'
        self.last_required_month = True  # Flag for previous months limit.
        self.driver = Selenium()

    # Close browser
    def close(self):
        self.driver.close_browser()

    # Open browser
    def open(self):
        driver = self.driver
        url = "https://apnews.com/"
        driver.open_available_browser(url, browser_selection='chrome')

    # Scraping through apnews.com
    def scrape(self):
        driver = self.driver
        v = Validator()
        self.open() # Open browser
        time.sleep(3)

        driver.click_element_if_visible("//*[contains(text(),  'I Accept')]")

        if not v.validate(driver, 'css:button.SearchOverlay-search-button', 10):
            driver.click_element_if_visible('css:.bx-close.bx-close-link.bx-close-inside')

        driver.click_element_if_visible('css:button.SearchOverlay-search-button')
        if not v.validate(driver, 'css:input.SearchOverlay-search-input', 10):
            return False
        search_box = driver.find_element('css:input.SearchOverlay-search-input')
        if search_box:
            time.sleep(2)
            driver.input_text(search_box, self.key)
            driver.press_keys(search_box, 'ENTER')

        if not v.validate(driver, 'css:main.SearchResultsModule-main', 10):
            return False
        time.sleep(2)
        driver.select_from_list_by_index('css:select.Select-input', '1')
        if not v.validate(driver, 'css:div.SearchFilter-heading', 10):
            return False

        driver.click_element('css:div.SearchFilter-heading')
        categories_section = driver.find_elements('css:ul.SearchFilter-items > li')

        for category in categories_section:  # Select a category
            section_text = v.get_text(driver, 'css:span', category)
            if section_text.lower().strip() == self.news_category:
                driver.click_element(driver.find_element('css:input[type="checkbox"]', category))
                time.sleep(2)
                break
            else:
                print('No categories were found: ', section_text)

        while self.last_required_month:  # Loop through the pages until there are no more news in the given range
            if not v.validate(driver, 'css:main.SearchResultsModule-main', 10):
                continue

            time.sleep(2)
            content = driver.find_element('css:main.SearchResultsModule-main')
            articles = driver.find_elements('css:.PageList-items > .PageList-items-item', content)
            articles.pop(0)

            self.get_news(articles)  # loop news method

            if self.last_required_month:
                driver.click_element('css:.Pagination-nextPage')
            else:
                print('No more news available in this range. End of process')

        self.insert_data(self.values)

    # Loop news articles
    def get_news(self, articles):
        driver = self.driver
        v = Validator()
        utils = Utils()

        for i in range(len(articles)):  # Loop through the articles extracting all the news information requested
            time.sleep(2)
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
                print(e)

            self.values.append([title, desc, date.replace('Updated ', ''),
                                phrase_count, does_it_have_currency_format, os.path.basename(name)])
            self.last_required_month = utils.validate_news_date_range(date, self.limit)
            if not self.last_required_month:
                break

    # It sends needed information in order to save it in a .xlsx file
    @staticmethod
    def insert_data(data: list):
        logger = Logger()
        logging = logger.get_logger()
        logging.info('Inserting rows in Excel file')
        filer = Filer()
        filer.create_excel()
        filer.insert_data(data=data, start_col=1, start_row=1)
        filer.save()
        logging.info('Excel file saved')
