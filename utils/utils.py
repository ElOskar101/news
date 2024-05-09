from RPA.Robocorp.WorkItems import WorkItems
from datetime import datetime, timedelta
import calendar
import random
import string
import re


class Utils:

    @staticmethod
    def get_work_items():
        """
        Gets work items from WorkItems.
        :return: work_items: WorkItems object (should be a dictionary key-value pairs)
        """
        work_items = WorkItems()
        work_items.get_input_work_item()
        work_item = work_items.get_work_item_variables()
        return work_item

    @staticmethod
    def count_phrase_occurrences(text, word):
        """
        Counts occurrences of a word in a text.
        :param text: The string we search in.
        :param word: The string we look for.
        :return: An Integer of how many occurrences of each word in text.
        """
        return sum(1 for w in text.split() if w == word)

    @staticmethod
    def validate_currency_format(text):
        """
        Validates a specific currency format fallowing these possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        :param text: The string we search in.
        :return: Boolean: True if the format matches, False otherwise.
        """
        #
        CURRENCY_PATTERN = r'^(\$?\d{1,3}(,\d{3})*(\.\d{1,2})?(\s*(dollars|USD))?|\d+\s*(dollars|USD))$'
        regex = re.compile(CURRENCY_PATTERN)
        match = regex.match(text)
        return bool(match)

    @staticmethod
    def validate_news_date_range(date, start_date, end_date):
        """
        Validates a date range fallowing this format: Published HH:mm PM CST, MM DD, YYYY
        :param date: The date is shown below the article
        :param start_date: Pre-calculated start date (see calculate_dates function)
        :param end_date: pre-calculated end date (see calculate_dates function)
        :return: Boolean: True if the date range matches, False otherwise.
        """
        if date.strip() == '' or date is None:
            return False
        if 'now' in date.lower() or 'ago' in date.lower():  # Means that date is x time ago (always current month)
            return True

        DATE_PATTERN = r"(\w+ \d{1,2}\, \d{4})$"
        date = re.findall(DATE_PATTERN, date)[0].strip()
        news_date = datetime.strptime(date, '%B %d, %Y')
        return start_date <= news_date <= end_date

    @staticmethod
    def generate_file_name():
        """
        Generate a random filename for pictures
        :return: random string within the limit of 7 characters
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

    @staticmethod
    def calculate_dates(limit):
        """
        Calculate range of dates based on limit.
         0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on
        :param limit: Integer representing how many months we consider to scrap. (0-1 for 1 month, 2 for 2 months...)
        :return: start_date = first day of the month we went back according limit, end_date = last day of current month
        """
        limit -= 1 if limit else limit  # Recalculates limit considering that 0 or 1 means the same
        current_date = datetime.now()
        start_date = current_date - timedelta(days=current_date.day - 1)
        _, last_day_of_month = calendar.monthrange(current_date.year, current_date.month)
        start_date -= timedelta(days=limit * 30)
        end_date = current_date.replace(day=last_day_of_month)

        return start_date, end_date


