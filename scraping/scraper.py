from RPA.Browser.Selenium import Selenium
import time
from utils.utils import Utils
from scraping.filer import Filer
import os
from utils.logging import Logger


class Scrapper:
    def __init__(self):
        self.values = []
        self.driver = Selenium()

    def close(self):
        self.driver.close_browser()

    def scrape(self):
        driver = self.driver
        utils = Utils()
        url = "https://apnews.com/"
        # url = 'https://apnews.com/search?q=airplanes&s=3'
        driver.open_available_browser(url, browser_selection='firefox')

        driver.click_element_if_visible('css:button.SearchOverlay-search-button')
        driver.element_should_be_visible('css:input.SearchOverlay-search-input')
        search_box = driver.find_element('css:input.SearchOverlay-search-input')
        if search_box:
            time.sleep(2)
            driver.input_text(search_box, "planes")
            driver.press_keys(search_box, 'ENTER')

        driver.wait_until_element_is_visible('css:main.SearchResultsModule-main', 10)
        time.sleep(2)
        driver.select_from_list_by_index('css:select.Select-input', '1')
        driver.wait_until_element_is_visible('css:main.SearchResultsModule-main', 10)
        
        driver.click_element('css:div.SearchFilter-heading')
        time.sleep(2)
        categories_section = driver.find_elements('css:ul.SearchFilter-items > li')
        # print(categories_section.text)
        for category in categories_section:
            section_text = driver.get_text(driver.find_element('css:span', category))
            if section_text.lower().strip() == 'stories':
                driver.click_element(driver.find_element('css:input[type="checkbox"]', category))
                break

        driver.wait_until_element_is_visible('css:main.SearchResultsModule-main', 10, 'Got an error')

        time.sleep(2)
        content = driver.find_element('css:main.SearchResultsModule-main')
        articles = driver.find_elements('css:.PageList-items > .PageList-items-item', content)
        articles.pop(0)
        for i in range(len(articles)):
            promo_content = driver.find_element('css:.PagePromo > .PagePromo-content', articles[i])
            title = driver.get_text(driver.find_element('css:div.PagePromo-title > a > span', promo_content))
            desc = driver.get_text(driver.find_element('css:.PagePromo-description', promo_content))
            date = driver.get_text(driver.find_element('css:.PagePromo-byline', promo_content))
            phrase_count = (utils.count_phrase_occurrences(title, 'airplanes')
                            + utils.count_phrase_occurrences(desc, 'airplanes'))
            does_it_have_currency_format = utils.validate_currency_format(title) or utils.validate_currency_format(desc)
            name = ''
            try:
                image = driver.find_element('css:img', articles[i])
                if image:
                    name = f"output/image{i}.png"
                    driver.screenshot(image, name)
                    time.sleep(1)
            except:
                pass
            (self.values.append([title, desc, date.replace('Updated ', ''),
                                 phrase_count, does_it_have_currency_format, os.path.basename(name)]))

        self.insert_data(self.values)

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
