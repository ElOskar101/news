import time
from scraping.scraper import Scrapper
from utils.logging import Logger


# Init instances of logging and driver. Call the other functions
def main():
    scraper = Scrapper()
    logging = Logger()
    logger = logging.get_logger()
    logger.info('Automation is starting')
    scraper.scrape()
    scraper.close()
    logger.info('Automation just finished')


if __name__ == "__main__":
    main()
