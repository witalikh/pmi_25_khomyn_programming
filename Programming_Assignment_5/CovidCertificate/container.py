from CovidCertificate.certificate import CovidCertificate
from CovidCertificate.certificate_validation import MultipleCertErrors, CertError

from Common.algorithms import quick_sort


class Container:
    """ Class for containing all Covid certificates"""

    def __init__(self):
        """
        Init container of Covid Certificates
        """
        self._records = []

    def __len__(self):
        """
        Dunder method, size of iterable
        :return: number of records in container
        """
        return len(self._records)

    def clear(self):
        """
        Clear all records in certificate
        """
        self._records.clear()
        return

    def __add__(self, other):
        """
        Dunder method of joining containers
        :param other: other container
        :return: joined containers
        """
        result = Container()

        result_list = self._records + other._records
        result._records = result_list

        return result

    def __iter__(self):
        """
        Dunder method of start iteration
        :return: object with additional attribute index
        """
        self.index = 0
        return iter(self._records)

    def __next__(self):
        """
        Dunder method of iteration jump
        :return: value after iteration jump
        """
        if self.index == len(self._records):
            raise StopIteration

        else:
            self.index += 1
            return self._records[self.index - 1]

    def __getitem__(self, item):
        """
        Dunder method of indexing without changing something
        :param item: index of certificate
        :return: certificate by index
        """
        return self._records[item]

    def __find__(self, identifier):
        """
        Private method of finding record index by identifier
        :param identifier: identifier for looking for the certificate
        :return: index where is the FIRST certificate with same identifier
        """
        for number, certificate in enumerate(self._records):
            if certificate.identifier == identifier:
                return number
        else:
            raise KeyError(f"there is no {identifier} in the records")

    def extend(self, iterable):
        """
        Extends container with iterable of certificates
        :param iterable: iterable to extend container with
        """
        # checking all elements
        for element in iterable:
            # checking types
            if isinstance(element, CovidCertificate):
                self._records.append(element)
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
        for certificate in self._records:
            for value in certificate.values():

                value = str(value)
                if entry.lower() in value.lower():
                    result_list.append(certificate)
                    break

        result._records = result_list
        return result

    def add_record(self, certificate: CovidCertificate):
        """
        Method to add certificate into container
        :param certificate: new certificate
        """
        self._records.append(certificate)

    def edit_record(self, identifier, key, value):
        """
        Method to edit some field in the certificate in container by identifier
        :param identifier: identifier for looking for the certificate
        :param key: field to change
        :param value: new value of field
        """
        assert key != "identifier"

        try:
            index = self.__find__(identifier)
            elem = self._records[index]

            kwargs = dict(elem)
            kwargs[key] = value

            # validate new value
            new_cert = CovidCertificate(**kwargs)
            self._records[index] = new_cert

        except KeyError:
            raise MultipleCertErrors(CertError.AbsentRecord())

    def delete_record(self, identifier):
        """
        Method of deleting record from container
        :param identifier: identifier for looking for the certificate
        """
        try:
            index = self.__find__(identifier)
            del self._records[index]
            return
        except KeyError:
            raise MultipleCertErrors(CertError.AbsentRecord())

    def sort(self, reverse=False, key=lambda x: x.identifier):
        """
        Method for quick_sort the container
        :param reverse: reverse sorting order demand
        :param key: element converter into comparable value
        """

        self._records = quick_sort(self._records, reverse, key)
        return
