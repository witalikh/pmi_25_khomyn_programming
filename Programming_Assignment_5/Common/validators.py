"""
File containing universal validators with return
And some provided default exceptions
"""
from Common.dates import Date, InvalidDate


class ValidateException(Exception):
    """ Universal base exception class"""
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


class Validate:
    """ Namespace class for common validators"""

    def __new__(cls):
        """ Forbid creating instances of this class """
        return None

    @staticmethod
    def pattern(pattern: str, custom_error=InvalidPatternString):
        """
        Decorator that matches first argument string with given strict pattern
        Usage: x are letters, y are digits.
        :param pattern: pattern to be matched with (in string)
        :param custom_error: exception to raise if invalid pattern
        :return: validated function that rejects wrong pattern
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):

            # first level wrap, intercepts function arguments
            def inner_wrapper(entry: str, *args, **kwargs):

                # try to convert into string if possible, it works only with strings
                if not isinstance(entry, str):
                    entry = str(entry)

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

                # everything is ok, function can be executed
                return func(entry, *args, **kwargs)

            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def name(min_words_count=2, max_words_count=3, custom_error=InvalidName):
        """
        Decorator that matches first function argument
        if it can be non-scientific unique name
        :param min_words_count: the least count of words in name
        :param max_words_count: the largest count of words in name
        :param custom_error: exception to raise if invalid format
        :return: wrapped function that rejects wrong name argument
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):

            # first level wrap, intercepts function arguments
            def inner_wrapper(entry: str, *args, **kwargs):

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

                # everything is ok except (perhaps cases mess)
                return func(entry.title(), *args, **kwargs)

            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def numeric(custom_error=NonNumeric):
        """
        Decorator that validates first argument for numeric string
        :param custom_error: exception to raise if invalid
        :return: wrapped function rejecting non-numeric first argument
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):
            def inner_wrapper(entry: str, *args, **kwargs):
                if not entry.isnumeric():
                    raise custom_error("entry is not completely numeric")
                else:
                    return func(entry, *args, **kwargs)

            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def date_format(custom_error=InvalidDate):
        """
        Function that validates a date
        :param custom_error: exception to raise if invalid format
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):

            # first level wrap, intercepts function arguments
            @Validate.pattern("yy.yy.yyyy", custom_error)
            def inner_wrapper(entry: str, *args, **kwargs):
                try:
                    day, month, year = entry.split(".")
                    date = Date(int(day), int(month), int(year))
                    return func(date, *args, **kwargs)

                except (InvalidDate, InvalidPatternString):
                    raise custom_error("chronological sequence violated")

            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def dates_sequence(start: Date, end: Date, custom_error=InvalidDateSequence):
        """
        Blocking function decorator checking two dates and raising Exception
        if chronological sequence is violated
        :param start: date supposed to be start
        :param end: date supposed to be end
        :param custom_error: exception to raise if invalid sequence
        :return: wrapped function enabling when chronological order is asserted
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):

            # first level wrap, intercepts function arguments
            def inner_wrapper(*args, **kwargs):
                if start > end:
                    raise custom_error(f"{str(start)} is later than {str(end)}")
                else:
                    return func(*args, **kwargs)

            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def belongs(container, custom_error=AssertionError):
        """
        Decorator checking if first argument belongs to container
        :param container: container ref to check if belongs
        :param custom_error: exception to raise if invalid sequence
        :return: wrapped function rejecting container non-members
        """

        # second level wrap, intercepts entire function
        def outer_wrapper(func):

            # first level wrap, intercepts function arguments
            def inner_wrapper(entry: str, *args, **kwargs):
                if entry in container:
                    return func(entry, *args, **kwargs)
                else:
                    raise custom_error(f"{entry} is not among the options")

            return inner_wrapper
        return outer_wrapper
