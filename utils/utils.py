from RPA.Robocorp.WorkItems import WorkItems
from datetime import datetime, timedelta
import calendar
import random
import string
import re


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def get_work_items():
        work_items = WorkItems()
        work_items.get_input_work_item()
        work_item = work_items.get_work_item_variables()
        return work_item

    @staticmethod
    def count_phrase_occurrences(text, word):
        return sum(1 for w in text.split() if w == word)

    @staticmethod
    def validate_currency_format(text):
        # possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        pattern = r'^(\$?\d{1,3}(,\d{3})*(\.\d{1,2})?(\s*(dollars|USD))?|\d+\s*(dollars|USD))$'
        regex = re.compile(pattern)
        match = regex.match(text)
        return bool(match)

    # Calculate the end date of the current month and the first day of the amount of months we want to back in
    @staticmethod
    def validate_news_date_range(date, limit):
        if date.strip() == '' or date is None:
            return False
        if not date.lower().startswith('updated'):  # Means that date is a minute | hours ago (always current month)
            return True
        pattern = r"(\w+ \d{1,2}\, \d{4})$"
        date = re.findall(pattern, date)[0].strip()
        news_date = datetime.strptime(date, '%B %d, %Y')
        current_date = datetime.now()
        start_date = current_date - timedelta(days=current_date.day - 1)
        _, last_day_of_month = calendar.monthrange(current_date.year, current_date.month)
        start_date -= timedelta(days=limit * 30)
        end_date = current_date.replace(day=last_day_of_month)
        return start_date <= news_date <= end_date

    @staticmethod
    def generate_file_name():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
