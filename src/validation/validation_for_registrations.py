"""
Data validation module during user registration .
"""
from datetime import datetime
import re


class ValidationRegistrations:

    def validation_name_surname_patronymic(self, text: str, max_len: int) -> bool:
        """
        Validation name, surname, patronymic

        :param max_len: int
        :return: bool
        """
        pattern = '^[А-Яа-яЁё]+$'
        return len(text) < max_len and \
            text[0].isupper() and \
            re.match(pattern, text) is not None

    def validation_data(self, date_string: str, format_date: str) -> bool:
        """
        Validation data

        :param date_string: str
        :param format_date: str
        :return: bool
        """
        try:
            datetime.strptime(date_string, format_date)
            return True
        except ValueError:
            return False
