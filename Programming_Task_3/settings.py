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

    # certificate_output
    cert_sep = "-" * 50
    cert_fancy_keywords = {
        "identifier": "Covid Certificate ID",
        "username": "Full name",
        "international_passport": "Passport code",
        "start_date": "issue date",
        "end_date": "Expire date",
        "date_of_birth": "Date of birth",
        "vaccine": "Vaccine"
    }

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
