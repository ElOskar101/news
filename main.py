from scraping.scraper import Scrapper
from utils.logging import Logger


def main():
    """Main function that runs the scraping process"""
    scraper = Scrapper()
    logging = Logger()
    logger = logging.get_logger()
    logger.info('Automation is starting...')
    scraper.scrape()
    scraper.close()
    logger.info('Automation just finished')


if __name__ == "__main__":
    main()
