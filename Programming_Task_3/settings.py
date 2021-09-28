"""
File for global settings of the program
Created for further flexibility
"""


class Globals:
    """
    Class of global values
    """

    def __new__(cls):
        """ Forbid creating instances of this class """
        return None

    # name parameters
    min_words_in_name = 2
    max_words_in_name = 3

    # passport parameters
    passport_pattern = "xxyyyyyy"

    min_passport_age = 14
    max_passport_age = 125

    # vaccination parameters
    min_vaccination_age = min_passport_age
    max_certificate_delay = 14

    available_vaccines = ["AstraZeneca", "Pfizer", "Moderna", "CoronaVac", "CoviShield"]
