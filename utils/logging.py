import logging


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def get_logger():
        return logging.getLogger('myapp.log')

    @staticmethod
    def set_logger():
        logging.basicConfig(filename='myapp.log', level=logging.INFO)

