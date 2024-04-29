from RPA.Robocorp.WorkItems import WorkItems
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
