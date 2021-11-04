"""
File containing simple server-side validators in form of functors
"""
import re


class ValidatePattern:
    """
    Functor class for validating string pattern
    Using Regular Expressions
    """
    def __init__(self, pattern: str):
        self.pattern = pattern

    def __call__(self, value):
        if not re.fullmatch(self.pattern, value):
            return False
        else:
            return True


class ValidateName:
    """
    Functor class for validating real name
    Based on word count limit and checking symbols different from letters and hyphens
    """
    def __init__(self, min_words=2, max_words=3):
        self.min_words = min_words
        self.max_words = max_words

    def __call__(self, value):
        words = value.split()
        if not (self.min_words <= len(words) <= self.max_words):
            return False

        for word in words:
            if not word.isalpha():
                sub_words = word.split("-")

                for sub_word in sub_words:
                    if not sub_word.isalpha():
                        return False
        else:
            return True
