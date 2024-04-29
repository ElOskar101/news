from abc import ABC, abstractmethod


class Sheet(ABC):
    @abstractmethod
    def __init__(self, title, desc, date, img_name, currency, match_phrase):
        self.title = title
        self.desc = desc
        self.date = date
        self.img_name = img_name
        self.currency = currency
        self.match_phrase = match_phrase

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def desc(self):
        pass

    @property
    @abstractmethod
    def date(self):
        pass

    @property
    @abstractmethod
    def img_name(self):
        pass

    @property
    @abstractmethod
    def currency(self):
        pass

    @property
    @abstractmethod
    def match_phrase(self):
        pass

    @title.setter
    def title(self, value):
        self._title = value

    @desc.setter
    def desc(self, value):
        self._desc = value

    @date.setter
    def date(self, value):
        self._date = value

    @img_name.setter
    def img_name(self, value):
        self._img_name = value

    @currency.setter
    def currency(self, value):
        self._currency = value

    @match_phrase.setter
    def match_phrase(self, value):
        self._match_phrase = value


class Sheet1(Sheet, ABC):
    def __init__(self, title, desc, date, img_name, currency, match_phrase):
        self.title = title
        self.desc = desc
        self.date = date
        self.img_name = img_name
        self.currency = currency
        self.match_phrase = match_phrase
