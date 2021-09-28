"""
File containing universal validators with return
And some provided default exceptions
"""
from dates import Date, InvalidDate


class ValidateException(Exception):
    """ Universal base exception class"""
    pass


class MismatchedString(ValidateException):
    """ Strings are different sizes """
    pass


class InvalidPatternString(ValidateException):
    """ String does not fit into the pattern """
    pass


class NonNumeric(ValidateException):
    """ String contains something apart from number """
    pass


class InvalidDateSequence(ValidateException):
    """ One date unexpectedly precedes other """
    pass


class InvalidName(ValidateException):
    """ Invalid name format """
    pass


class WrongChoice(ValidateException):

    pass


class Validate:
    """ Namespace class for common validators"""

    def __new__(cls):
        """ Forbid creating instances of this class """
        return None

    @staticmethod
    def pattern(entry: str, pattern: str, custom_error=InvalidPatternString):
        """
        Function that matches input string with given strict pattern
        Usage: x are letters, y are digits.
        :param entry: string to check
        :param pattern: pattern to be matched with (in string)
        :param custom_error: exception to raise if invalid pattern
        :return: validated string or exception if invalid
        """

        # mismatching sized string cannot fit into pattern
        if len(entry) != len(pattern):
            raise custom_error(f"Symbols count mismatch: {len(entry)} and {len(pattern)}")

        # checking every position to pattern
        for position, (symbol, template) in enumerate(zip(entry, pattern)):
            if template.lower() == 'x':
                if not symbol.isalpha():
                    raise custom_error(f"Expected symbol in position {position}.")

            elif template.lower() == 'y':
                if not symbol.isdigit():
                    raise custom_error(f"Expected digit in position {position}.")

            elif template != symbol:
                raise custom_error(f"Expected symbol {template} in position {position}.")

            else:
                continue

        # everything is ok, return
        return entry

    @staticmethod
    def name(entry: str, min_words_count=2, max_words_count=3, custom_error=InvalidName):
        """
        Function that validates any non-scientific name that can be unique
        :param entry: string to check
        :param min_words_count: the least count of words in name
        :param max_words_count: the largest count of words in name
        :param custom_error: exception to raise if invalid format
        :return: capitalized valid name or custom_error if totally invalid
        """

        words = entry.split()
        if not (min_words_count <= len(words) <= max_words_count):
            raise custom_error(f" too many name words: {len(words)}")

        # checking if names contain only letters or hyphens
        for word in words:
            if not word.isalpha():
                # name still can be valid due to hyphens
                sub_words = word.split("-")

                for sub_word in sub_words:
                    if not sub_word.isalpha():
                        # obviously wrong format
                        raise custom_error(" name cannot contain other symbols than letters and hyphens")

        # everything is ok except perhaps cases mess
        return entry.title()

    @staticmethod
    def numeric(entry: str, custom_error=NonNumeric):
        """
        Function that validates numeric string
        :param entry: string to check if it contains only numbers
        :param custom_error: exception to raise if invalid
        :return:
        """
        if not entry.isnumeric():
            raise custom_error("entry is not completely numeric")
        else:
            return entry

    @staticmethod
    def choice(choices, entry: str, start=0, custom_error=WrongChoice):
        """
        Function that validates choice query
        :param choices: number of available options
        :param entry: string to validate
        :param start: start choice number
        :param custom_error: exception to raise if invalid
        :return:
        """
        try:
            number = int(entry)

            # checking range
            if not start <= number < start + choices:
                raise custom_error(f"alternative {number} is absent")

            else:
                return number

        # ValueError can happen not only from that reason, let's redefine
        except ValueError:
            raise custom_error(f"the format is incorrect")

    @staticmethod
    def date_format(entry: str, custom_error=InvalidDate):
        """
        Function that validates a date
        :param entry:
        :param custom_error: exception to raise if invalid format
        :return:
        """
        try:
            validated_entry = Validate.pattern(entry, "yy.yy.yyyy")
            day, month, year = validated_entry.split(".")

            return Date(int(day), int(month), int(year))

        except (InvalidDate, InvalidPatternString):
            raise custom_error

    @staticmethod
    def dates_sequence(start: Date, end: Date, custom_error=InvalidDateSequence):
        """
        Function that compares two dates and raises Error
        if chronological sequence is violated
        :param start: date supposed to be start
        :param end: date supposed to be end
        :param custom_error: exception to raise if invalid sequence
        :return: custom_error if invalid
        """
        if start > end:
            raise custom_error(f"{str(start)} is later than {str(end)}")
        else:
            return
