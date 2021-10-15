"""
Main file. Implementation of CovidCertificate and its container
"""
from CovidCertificate.certificate_validation import validate_certificate
from settings import Globals


class CovidCertificate:
    @validate_certificate
    def __init__(self,
                 identifier: str, username: str, international_passport: str,
                 start_date: str, end_date: str, date_of_birth: str, vaccine: str):
        """
        Initializes Covid Certificate object
        """

        self.identifier = identifier

        self.username = username
        self.international_passport = international_passport

        self.start_date = start_date
        self.end_date = end_date
        self.date_of_birth = date_of_birth

        self.vaccine = vaccine

    def __str__(self):
        """
        Dunder method of fancy string representation
        :return: fancy string
        """
        result = Globals.cert_sep + '\n'
        for key, value in self.__dict__.items():
            result += Globals.cert_fancy_keywords[key] + ': ' + str(value) + "\n"

        result += Globals.cert_sep
        return result

    # making dict() method possible on this

    def __iter__(self):
        """
        Dunder method of creating iterator, for dict() overload
        :return: generator which give a key-value pair on each iteration
        """
        for key, value in self.__dict__.items():
            yield key, value

    # overloading **unpack

    @staticmethod
    def keys():
        """
        Dunder method to get keys in certificate
        :return: keys tuple
        """
        return ("identifier", "username", "international_passport",
                "date_of_birth", "start_date", "end_date", "vaccine")

    def items(self):
        """
        Method to get pairs of key and value
        :return: key, value pairs list
        """
        items_list = []
        for key in self.keys():
            items_list.append((key, self.__dict__[key]))

        return items_list

    def values(self):
        """
        Method to get values
        :return: values list
        """
        values_list = []
        for key in self.keys():
            values_list.append(self.__dict__[key])

        return values_list

    def __getitem__(self, key):
        """
        Dunder method to get values from keys in certificate
        :param key: key to access field of class
        :return: value of the key
        """
        return self.__dict__[key]
