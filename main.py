import time
from scraping.scraper import Scrapper
from utils.logging import Logger


# Init instances of logging and driver. Call the other functions
def main():
    scraper = Scrapper()
    logger = Logger()

    logger.set_logger()
    logging = logger.get_logger()
    logging.info('Automation is starting')
    scraper.scrape()
    logging.info('Automation just finished')
    time.sleep(1)
    scraper.close()


if __name__ == "__main__":
    main()
