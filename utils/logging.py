import logging


class Logger:
    def __init__(self):
        self.filename = 'myapp.log'
        self.console_handler = logging.StreamHandler()

    def get_logger(self):
        logging.basicConfig(filename=self.filename, level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        self.console_handler.setFormatter(formatter)

        logger = logging.getLogger(self.filename)
        if not logger.handlers:
            logger.addHandler(self.console_handler)

        return logger

