"""
File containing everything about CovidCertificate validation
Such as certificate validator and Exceptions
"""

from validators import Validate
from dates import get_today_date


from settings import Globals


class CertificateException(Exception):
    """ Base exception class for exceptions of certificate """
    pass


class MultipleCertErrors(Exception):
    """ Exception class containing list of exceptions """

    def __init__(self, *args):
        """

        :param args:
        """
        self.container = list(args)

    def __len__(self):

        return len(self.container)

    def append(self, obj):

        self.container.append(obj)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.container):
            raise StopIteration
        else:
            self.index += 1
            return self.container[self.index - 1]


class CertError:
    """ Namespace class for containing exceptions"""

    class InvalidIdentifier(CertificateException):
        """ Identifier is incorrect formatted """
        pass

    class InvalidName(CertificateException):
        """ Name is incorrect formatted """
        pass

    class InvalidPassport(CertificateException):
        """ Passport is incorrect formatted"""
        pass

    class InvalidBirthDateFormat(CertificateException):
        """ Date of birth is incorrect formatted """
        pass

    class InvalidStartDateFormat(CertificateException):
        """ Start date is incorrect formatted"""
        pass

    class InvalidEndDateFormat(CertificateException):
        """ End date is incorrect formatted """
        pass

    class TooYoungAge(CertificateException):
        """ Current age is insufficient for passport """
        pass

    class TooOldAge(CertificateException):
        """ Age is presumed to be impossible due to big value"""
        pass

    class InvalidStartDate(CertificateException):
        """ Covid certificate cannot start its action in this date """
        pass

    class InvalidEndDate(CertificateException):
        """ Covid certificate cannot last to this date"""
        pass

    class InvalidVaccine(CertificateException):
        """ Vaccine is absent or not recommended """
        pass

    class AbsentRecord(CertificateException):
        """ No record found in collection """
        pass


class CertificateValidation:
    """ Class for validation certificate fields"""

    def __next__(self):
        """ Forbid creation class instances """
        return None

    @staticmethod
    def validate_formats(func):
        """
        Helper decorator for validating fields format
        """

        validators = {
            "identifier": Validate.numeric,
            "username": Validate.name,
            "international_passport": Validate.pattern,
            "date_of_birth": Validate.date_format,
            "start_date": Validate.date_format,
            "end_date": Validate.date_format,
            "vaccine": Validate.belongs
        }

        arguments = {
            "identifier": {
                "custom_error": CertError.InvalidIdentifier
            },

            "username": {
                "min_words_count": Globals.min_words_in_name,
                "max_words_count": Globals.max_words_in_name,
                "custom_error": CertError.InvalidName
            },

            "international_passport": {
                "pattern": Globals.passport_pattern,
                "custom_error": CertError.InvalidPassport
            },

            "date_of_birth": {
                "custom_error": CertError.InvalidBirthDateFormat
            },

            "start_date": {
                "custom_error": CertError.InvalidStartDateFormat
            },

            "end_date": {
                "custom_error": CertError.InvalidEndDateFormat
            },

            "vaccine": {
                           "container": Globals.available_vaccines,
                           "custom_error": CertError.InvalidVaccine
                       }
        }

        def wrapper(*args, **kwargs):

            valid_fields = {}
            error_log = MultipleCertErrors()

            # for every value of field
            for key, value in kwargs.items():
                try:
                    # dynamic decorator
                    decorator = validators[key](**arguments[key])

                    # decorator interception function
                    @decorator
                    def obtain_validated_value(entry):
                        return entry

                    # validation
                    valid_fields[key] = obtain_validated_value(value)

                # collecting errors into one exception
                except CertificateException as instance:
                    error_log.append(instance)

            # execute function if no errors happened
            if len(error_log) == 0:
                return func(*args, **valid_fields)

            else:
                raise error_log

        return wrapper

    @staticmethod
    def validate_dependent(func):
        """
        Helper decorator for validating mutually dependent fields
        """

        def wrapper(*args, **kwargs):
            today = get_today_date()

            prerequisites = {
                "min_passport": today.subtract(years=Globals.min_passport_age),
                "max_passport": today.subtract(years=Globals.max_passport_age),
                "certificate_delay": today.add(days=Globals.max_certificate_delay),
                "min_vaccination_date": kwargs["date_of_birth"].add(years=Globals.min_vaccination_age)
            }

            validator = Validate.dates_sequence

            dependencies = [
                (kwargs["date_of_birth"], prerequisites["min_passport"], CertError.TooYoungAge),
                (prerequisites["max_passport"], kwargs["date_of_birth"], CertError.TooOldAge),
                (prerequisites["min_vaccination_date"], kwargs["start_date"], CertError.InvalidStartDate),
                (kwargs["start_date"], prerequisites["certificate_delay"], CertError.InvalidStartDate),
                (kwargs["start_date"], kwargs["end_date"], CertError.InvalidEndDate)
            ]

            error_log = MultipleCertErrors()

            # checking every dependency
            for argument_set in dependencies:
                try:
                    # dynamic decorator
                    decorator = validator(*argument_set)

                    @decorator
                    def check_chronology():
                        pass

                    # validation
                    check_chronology()

                # collecting errors into one exception
                except CertificateException as instance:
                    error_log.append(instance)

            # execute function if no errors happened
            if len(error_log) == 0:
                return func(*args, **kwargs)
            else:
                raise error_log

        return wrapper

    @staticmethod
    def validate_certificate(func):
        """
        Decorator for validating all the fields of certificate
        Raises MultipleCertErrors if something is incorrect
        :return:
        """

        @CertificateValidation.validate_formats
        @CertificateValidation.validate_dependent
        def wrapper(*args, **kwargs):

            # everything is ok, return
            return func(*args, **kwargs)

        return wrapper
