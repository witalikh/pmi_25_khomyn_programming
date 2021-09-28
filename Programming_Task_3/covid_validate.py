"""
File containing everything about CovidCertificate validation
Such as certificate validator and Exceptions
"""

from validators import Validate
from dates import Date, get_today_date


from settings import Globals


class CertificateException(Exception):
    """ Base exception class for exceptions of certificate """
    pass


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
    """ Functor class for validation certificate fields"""

    @staticmethod
    def validate_fields(identifier, username, international_passport,
                        start_date, end_date, date_of_birth, vaccine):
        """
        Function for validating all the fields of certificate
        Raises according CertificateException if something is incorrect
        :return:
        """

        # validate identifier
        Validate.numeric(identifier, CertError.InvalidIdentifier)

        # validate name
        Validate.name(username, Globals.min_words_in_name, Globals.max_words_in_name,
                      CertError.InvalidName)

        # validate passport
        Validate.pattern(international_passport, Globals.passport_pattern,
                         CertError.InvalidPassport)

        # validate dates format
        format_date = Validate.date_format

        valid_birth = date_of_birth
        valid_start = start_date
        valid_end = end_date

        if not isinstance(date_of_birth, Date):
            valid_birth = format_date(date_of_birth, CertError.InvalidBirthDateFormat)

        if not isinstance(start_date, Date):
            valid_start = format_date(start_date, CertError.InvalidStartDateFormat)

        if not isinstance(end_date, Date):
            valid_end = format_date(end_date, CertError.InvalidEndDateFormat)

        # validate dates chronology
        # preparations
        check_chronology = Validate.dates_sequence
        today = get_today_date()

        # range of dates when anybody can have a passport:
        min_passport = today.subtract(years=Globals.min_passport_age)
        max_passport = today.subtract(years=Globals.max_passport_age)

        # check chronologies with birthdays and passport range
        check_chronology(valid_birth, min_passport, CertError.TooYoungAge)
        check_chronology(max_passport, valid_birth, CertError.TooOldAge)

        # range of dates when vaccination certificate can be started
        min_vaccination_date = valid_birth.add(years=Globals.min_vaccination_age)
        certificate_delay = today.add(days=Globals.max_certificate_delay)

        # check chronologies with start day and certificate validity range
        check_chronology(min_vaccination_date, valid_start, CertError.InvalidStartDate)
        check_chronology(valid_start, certificate_delay, CertError.InvalidStartDate)

        # check end date if it not precedes start date
        check_chronology(valid_start, valid_end, CertError.InvalidEndDate)

        # vaccine validation: looking in global vaccine list
        if vaccine not in Globals.available_vaccines:
            raise CertError.InvalidVaccine

        # everything is ok, return
        return
