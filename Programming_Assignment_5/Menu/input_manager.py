"""
File for input manager class implementation
Specified for Covid Certificates
"""

from CovidCertificate.certificate import CovidCertificate
from CovidCertificate.certificate_validation import CertError, MultipleCertErrors

from Common.json_manager import JSONManager
from Menu.interface_messages import InterfaceMessages

from copy import deepcopy


class InputManager:
    """ Class managing input processes"""

    def __init__(self, messages: InterfaceMessages):
        self.messages = messages

    def get_exception_message(self, exception):
        """
        Prints message depending on exception
        :param exception: any Exception object
        :return:
        """
        dict_of_excepts = {

            CertError.AbsentRecord: self.messages.absent_record,

            CertError.InvalidIdentifier: self.messages.wrong_identifier,
            CertError.InvalidName: self.messages.wrong_name,
            CertError.InvalidPassport: self.messages.wrong_passport,

            CertError.InvalidStartDateFormat: self.messages.wrong_start_date_format,
            CertError.InvalidEndDateFormat: self.messages.wrong_end_date_format,
            CertError.InvalidBirthDateFormat: self.messages.wrong_birth_date_format,

            CertError.TooYoungAge: self.messages.wrong_birth_date_young,
            CertError.TooOldAge: self.messages.wrong_birth_date_young,

            CertError.InvalidStartDate: self.messages.wrong_start_date,
            CertError.InvalidEndDate: self.messages.wrong_end_date,

            CertError.InvalidVaccine: self.messages.wrong_vaccine,
        }

        return dict_of_excepts[exception.__class__]

    def get_message_from_parameter(self, parameter):
        """
        Method of getting message for parameter input (query 4)
        :param parameter: parameter that should be inputted
        :return: message of input require
        """
        dict_of_param_messages = {
            "identifier": self.messages.identifier_input,
            "username": self.messages.name_input,
            "international_passport": self.messages.passport_input,
            "date_of_birth": self.messages.birth_date_input,
            "start_date": self.messages.start_date_input,
            "end_date": self.messages.end_date_input,
            "vaccine": self.messages.vaccine_input
        }

        return dict_of_param_messages[parameter]

    def input_identifier(self):
        """
        Method to input identifier (for queries 4, 5)
        :return:
        """

        # perpetual input of correct identifier
        while True:

            identifier = input(self.messages.search_by_identifier)
            if identifier.isnumeric():
                return identifier
            else:
                print(self.messages.wrong_identifier)

    def input_parameter(self):
        """
        Method to input parameter (for queries 4 and 6)
        :return: valid actual parameter name
        """

        # parameter names in interface slightly differ
        parameters = {
            "id": "identifier",
            "name": "username",
            "passport": "international_passport",
            "birthday": "date_of_birth",
            "start date": "start_date",
            "end date": "end_date",
            "vaccine": "vaccine"
        }

        # Asking parameter input
        print(self.messages.parameter_choices)
        entry = input(self.messages.parameter_input)

        # find a matching and return or repeat
        if entry.strip() in parameters.keys():
            return parameters[entry.strip()]

        # messages that wrong parameter is entered
        else:
            print(self.messages.wrong_parameter)
            print(self.messages.parameter_choices)
            return None

    def input_certificate(self):
        """
        Complete method for inputting entire certificate manually
        :return: certificate if success or None if not
        """
        while True:
            try:
                params = CovidCertificate.keys()
                kwargs = {}

                for key in params:
                    kwargs[key] = input(self.get_message_from_parameter(key))

                result = CovidCertificate(**kwargs)

            except MultipleCertErrors as instances:
                for instance in instances:
                    print(self.get_exception_message(instance))
                return None

            except FileNotFoundError:
                pass

            else:
                return result

    def log_errors(self, filename: str, obj: dict, exception: Exception):
        """
        Method for registering all errors into separate log file
        :param filename: file where exception happened
        :param obj: trouble object in form of dictionary
        :param exception: exception where it happened
        """

        log_file = filename.replace(".", "_") + "_error_log.json"
        json_manager = JSONManager(log_file)

        errors = []
        if isinstance(exception, MultipleCertErrors):
            errors = [self.get_exception_message(err) for err in exception]

        log_obj = deepcopy(obj)
        log_obj["errors"] = errors

        json_manager.extend_info([log_obj])
        return
