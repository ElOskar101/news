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
        self.driver = Selenium()

    def close(self):
        self.driver.close_browser()

    # Scraping through apnews.com
    def scrape(self):
        driver = self.driver
        v = Validator()
        utils = Utils()
        limit = 0
        key = 'mosquito'
        last_required_month = True  # Flag for previous months limit. Must be false in case there are no more month left
        url = "https://apnews.com/"
        # url = f'https://apnews.com/search?q={key}&s=3'
        driver.open_available_browser(url, browser_selection='firefox')

        driver.click_element_if_visible('css:button.SearchOverlay-search-button')
        if not v.validate(driver, 'css:input.SearchOverlay-search-input', 10):
            return False
        search_box = driver.find_element('css:input.SearchOverlay-search-input')
        if search_box:
            time.sleep(2)
            driver.input_text(search_box, "mosquito")
            driver.press_keys(search_box, 'ENTER')

        if not v.validate(driver, 'css:main.SearchResultsModule-main', 10):
            return False
        time.sleep(2)
        driver.select_from_list_by_index('css:select.Select-input', '1')
        if not v.validate(driver, 'css:div.SearchFilter-heading', 10):
            return False

        driver.click_element('css:div.SearchFilter-heading')
        categories_section = driver.find_elements('css:ul.SearchFilter-items > li')

        for category in categories_section:
            section_text = v.get_text(driver, 'css:span', category)
            if section_text.lower().strip() == 'stories':
                driver.click_element(driver.find_element('css:input[type="checkbox"]', category))
                break
            else:
                print('No categories were found: ', section_text)

        while last_required_month:
            if not v.validate(driver, 'css:main.SearchResultsModule-main', 10):
                continue

            time.sleep(2)
            content = driver.find_element('css:main.SearchResultsModule-main')
            articles = driver.find_elements('css:.PageList-items > .PageList-items-item', content)
            articles.pop(0)
            for i in range(len(articles)):
                promo_content = driver.find_element('css:.PagePromo > .PagePromo-content', articles[i])
                title = v.get_text(driver, 'css:div.PagePromo-title > a > span', promo_content)
                desc = v.get_text(driver, 'css:.PagePromo-description', promo_content)
                date = v.get_text(driver, 'css:.PagePromo-byline', promo_content)
                phrase_count = (utils.count_phrase_occurrences(title, key)
                                + utils.count_phrase_occurrences(desc, key))
                does_it_have_currency_format = (utils.validate_currency_format(title)
                                                or utils.validate_currency_format(desc))
                name = ''

                try:
                    image = driver.find_element('css:img', articles[i])
                    alt_name = driver.get_element_attribute(image, 'alt')
                    if image:
                        name = f"output/image-{utils.generate_file_name()}.png"
                        driver.screenshot(image, name)
                        time.sleep(1)
                except:
                    pass

                self.values.append([title, desc, date.replace('Updated ', ''),
                                    phrase_count, does_it_have_currency_format, os.path.basename(name)])
                last_required_month = utils.validate_news_date_range(date, limit)
            if last_required_month:
                driver.click_element('css:.Pagination-nextPage')
            else:
                print('No more news available in this range')

        self.insert_data(self.values)

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
