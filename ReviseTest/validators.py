import os
import re
import datetime


class ValidationError(Exception):
    pass


class Validators:

    @staticmethod
    def any(entry):
        try:
            return entry
        except (ValueError, TypeError):
            raise ValidationError

    @staticmethod
    def is_numeric(entry: str):
        if isinstance(entry, int) or entry.isnumeric():
            return int(entry)
        else:
            raise ValidationError()

    @staticmethod
    def is_alpha(entry: str):
        words = entry.split()
        if_letters = [word.isalpha() for word in words]

        if all(if_letters):
            return entry.title()
        else:
            raise ValidationError()

    @staticmethod
    def is_filename(entry: str):
        if os.path.isfile(entry):
            return entry
        else:
            raise FileNotFoundError

    @staticmethod
    def is_datetime(entry: str):
        try:
            return datetime.datetime.fromisoformat(entry)
        except ValueError:
            raise ValidationError

    @staticmethod
    def is_date(entry: str):
        try:
            return datetime.date.fromisoformat(entry)
        except ValueError:
            raise ValidationError

    @staticmethod
    def is_time(entry: str):
        try:
            return datetime.time.fromisoformat(entry)
        except ValueError:
            raise ValidationError

    class BetweenMatch:

        def __init__(self, _prev, _next, _type=str):
            self.prev = _prev
            self.next = _next

            self.type = _type

        def __call__(self, curr):
            typed_curr = self.type(curr)

            if self.prev is not None and self.prev > typed_curr:
                raise ValidationError

            if self.next is not None and self.next < typed_curr:
                raise ValidationError

            return typed_curr

    class PatternMatch:
        def __init__(self, pattern: str):
            self.pattern = pattern

        def __call__(self, entry: str):
            if re.fullmatch(self.pattern, str(entry)):
                return entry
            else:
                raise ValidationError

    class BelongMatch:
        def __init__(self, iterable):
            self.iterable = iterable

        def __call__(self, entry: str):
            if entry not in self.iterable:
                raise ValidationError
            else:
                return entry

    class TypeMatch:

        def __init__(self, _type):
            self.type = _type

        def __call__(self, entry):
            try:
                return self.type(entry)

            except (ValueError, TypeError):
                raise ValidationError
