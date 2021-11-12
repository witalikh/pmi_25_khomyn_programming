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
        for key in self.keys():
            result += Globals.cert_fancy_keywords[key] + ': ' + str(getattr(self, key)) + "\n"

        result += Globals.cert_sep
        return result

    # making dict() method possible on this

    def __iter__(self):
        """
        Dunder method of creating iterator, for dict() overload
        :return: generator which give a key-value pair on each iteration
        """
        for key, value in self.items():
            yield key, value

    @staticmethod
    def keys():
        """
        Get keys in certificate
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
            items_list.append((key, getattr(self, key)))

        return items_list

    def values(self):
        """
        Method to get values
        :return: values list
        """
        values_list = []
        for key in self.keys():
            values_list.append(getattr(self, key))

        return values_list

    def __getitem__(self, key):
        """
        Get values from keys in certificate
        :param key: key to access field of class
        :return: value of the key
        """
        return getattr(self, key)

    def __eq__(self, other):
        """
        (==) Checks if certificates are equal
        :return: True/False
        """
        for key, value in self.items():
            if getattr(other, key) != value:
                return False
        else:
            return True

    def __ne__(self, other):
        """
        (!=) Checks if certificates are not equal
        :return: True/False
        """
        return not self == other
