import time
from scraping.scraper import Scrapper
from utils.logging import Logger


def main():
    scraper = Scrapper()
    logger = Logger()

    logger.set_logger()
    logging = logger.get_logger()
    logging.info('Automation is starting')
    scraper.scrape()
    logging.info('Automation just finished')
    # time.sleep(300)
    scraper.close()


if __name__ == "__main__":
    main()

# TODO:
# Accept cookies
# Validate elements were not found
