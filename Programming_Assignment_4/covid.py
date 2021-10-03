"""
Main file. Implementation of CovidCertificate and its container
"""

from covid_validate import CertError, MultipleCertErrors, CertificateValidation
from algorithms import quick_sort

from settings import Globals


class CovidCertificate:
    @CertificateValidation.validate_certificate
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


class Container:
    """ Class for containing all CoViD certificates"""

    def __init__(self):
        self.records = []

    def __add__(self, other):
        """
        Dunder method of joining containers
        :param other: other container
        :return: joined containers
        """
        result = Container()

        result_list = self.records + other.records
        result.records = result_list

        return result

    # overloading for ... in ...
    def __iter__(self):
        """
        Dunder method of start iteration
        :return: object with additional attribute index
        """
        self.index = 0
        return iter(self.records)

    def __next__(self):
        """
        Dunder method of iteration jump
        :return: value after iteration jump
        """
        if self.index == len(self.records):
            raise StopIteration

        else:
            self.index += 1
            return self.records[self.index - 1]

    def __getitem__(self, item):
        """
        Dunder method of indexing without changing something
        :param item: index of certificate
        :return: certificate by index
        """
        return self.records[item]

    def __find__(self, identifier):
        """
        Private method of finding record index by identifier
        :param identifier: identifier for looking for the certificate
        :return: index where is the FIRST certificate with same identifier
        """
        for number, certificate in enumerate(self.records):
            if certificate.identifier == identifier:
                return number
        else:
            raise KeyError(f"there is no {identifier} in the records")

    def extend(self, iterable):
        """
        Extends container with iterable of certificates
        :param iterable: iterable to extend container with
        :return:
        """
        # checking all elements
        for element in iterable:
            # checking types
            if isinstance(element, CovidCertificate):
                self.records.append(element)
            else:
                raise TypeError(f"expected only CovidCertificate objects in iterable")

    def find_all(self, entry):
        """
        Method for finding any matching in any field
        :param entry: entry string that should be matching with anything
        :return: CovidCertificatesContainer
        """
        result = Container()
        result_list = []
        for certificate in self.records:
            for value in certificate.values():

                value = str(value)
                if entry.lower() in value.lower():
                    result_list.append(certificate)
                    break

        result.records = result_list
        return result

    def add_record(self, certificate: CovidCertificate):
        """
        Method to add certificate into container
        :param certificate: new certificate
        :return:
        """

        self.records.append(certificate)

    def edit_record(self, identifier, key, value):
        """
        Method to edit some field in the certificate in container by identifier
        :param identifier: identifier for looking for the certificate
        :param key: field to change
        :param value: new value of field
        :return:
        """
        assert key != "identifier"

        try:
            index = self.__find__(identifier)
            elem = self.records[index]

            kwargs = dict(elem)
            kwargs[key] = value

            # validate new value
            CertificateValidation.validate_certificate(CovidCertificate.__init__)(elem, **kwargs)

            elem.__dict__[key] = value

        except KeyError:
            raise MultipleCertErrors(CertError.AbsentRecord())

    def delete_record(self, identifier):
        """
        Method of deleting record from container
        :param identifier: identifier for looking for the certificate
        :return:
        """
        try:
            index = self.__find__(identifier)
            del self.records[index]
            return
        except KeyError:
            raise MultipleCertErrors(CertError.AbsentRecord())

    def sort(self, reverse=False, key=lambda x: x.identifier):
        """
        Method for quick_sort the container
        :param reverse: reverse sorting order demand
        :param key: element converter into comparable value
        :return:
        """

        self.records = quick_sort(self.records, reverse, key)
        return
