import logging


class Logger:
    def __init__(self):
        """
        Initialize the logger
        """
        self.filename = 'myapp.log'
        self.console_handler = logging.StreamHandler()

    def get_logger(self):
        """
        Set up the logger and set it handler in order to show messages in console only if it does not exist
        :return: logger: logger object
        """
        logging.basicConfig(filename=self.filename, level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        self.console_handler.setFormatter(formatter)

        logger = logging.getLogger(self.filename)
        if not logger.handlers:
            logger.addHandler(self.console_handler)

        return logger

