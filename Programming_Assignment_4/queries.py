"""
File for processing queries with CovidCertificates
"""
from covid import CovidCertificate, Container
from covid_validate import CertError, MultipleCertErrors

from input_manager import InputManager
from file_manager import FileManager

from interface_messages import InterfaceMessages

from validators import Validate


class ImmediateExit(Exception):
    """ Class for force exit """
    pass


class WrongOption(Exception):
    """ Class for wrong option """


class CertificatesQueriesThread:
    """ Class responsible for managing sequent queries """

    def __init__(self, database, messages: InterfaceMessages):
        """
        Initialize
        :param database: file which serves as CoViD-19 certificates database
        :param messages: object of class with strings for menu
        """
        # initial configurations
        self.container = Container()

        # managers
        self.file_manager = FileManager(database)
        self.input_manager = InputManager(messages)

        # messages
        self.messages = messages
        self.counter = 0

        # load database before start
        self.load_database()

    def load_database(self):
        """
        Method of extracting data into container
        :return:
        """
        result = self.file_manager.extract_info(CovidCertificate)
        self.container.extend(result)
        return

    def append_to_database(self, **kwargs):
        """
        Append database quickly
        :param kwargs: keyword arguments to append to database
        :return:
        """
        self.file_manager.append_info(**kwargs)
        return

    def update_database(self):
        """
        Method of updating file records
        :return:
        """
        self.file_manager.clear_info()
        self.file_manager.extend_info(self.container)
        return

    def query_0(self):
        """
        Exit from program, so close it properly
        :return:
        """
        print(self.messages.exit_message)
        raise ImmediateExit

    def query_1(self):
        """
        Print all certificates in database
        :return:
        """
        print(self.messages.all_certificates)
        for certificate in self.container:
            print(certificate)

        return

    def query_2(self):
        """
        Find any matching with any field in all certificates and print certificates
        :return:
        """
        # what should we find
        entry = input(self.messages.entry_input)

        # find all entries
        result = self.container.find_all(entry)

        # print all matches
        print(self.messages.matching_certificates(entry))
        for certificate in result:
            print(certificate)

        return

    def query_3(self):
        """
        Input certificate manually and write it to file
        :return:
        """
        # input certificate
        certificate = self.input_manager.input_certificate()

        # if certificate is ready to append
        if certificate:
            self.container.add_record(certificate)

            # append the database
            self.append_to_database(**certificate)

            # print certificate
            print(self.messages.appended_certificate)
            print(certificate)

        return

    def query_4(self):
        """
        Edit the record in according place and rewrite the file
        :return:
        """

        # Obtaining valid identifier and parameter
        identifier = self.input_manager.input_identifier()
        parameter = self.input_manager.input_parameter()

        # asserting identifier change
        if parameter == "identifier":
            print(self.messages.identifier_change)
            return

        # perpetual input of value until done
        while True:
            value = input(self.input_manager.get_message_from_parameter(parameter))

            # try to edit the record
            try:
                self.container.edit_record(identifier, parameter, value)

            except MultipleCertErrors as instances:
                # any CertificateException can occur, print according message

                for instance in instances:
                    print(self.input_manager.get_exception_message(instance))
                return

            # update the database if success
            else:
                self.update_database()
                return

    def query_5(self):
        """
        Delete the record from container
        :return:
        """
        identifier = self.input_manager.input_identifier()

        # delete if record exists
        try:
            self.container.delete_record(identifier)

        # ignore if record doesnt exist
        except MultipleCertErrors as instances:
            for instance in instances:
                print(self.input_manager.get_exception_message(instance))
            return

        # update database if success
        else:
            # edit the file if possible
            self.update_database()
            return

    def query_6(self):
        """
        Sort container by parameter and show it
        :return:
        """
        parameter = self.input_manager.input_parameter()

        # getting custom key from parameter
        def custom_key(param):
            return lambda x: x.__dict__[param]

        # sort by parameter
        self.container.sort(key=custom_key(parameter))

        # print all certificates
        print(self.messages.sorted_certificates)
        for certificate in self.container:
            print(certificate)

        # update database
        self.update_database()
        return

    def wrong_query(self):
        """
        User entered wrong query, warn him about it
        :return:
        """
        print(self.messages.wrong_query)
        print()
        print(self.messages.menu_choices)

    def process_query(self, query):
        """
        Accepting query and performing actions
        :param query: query to process
        :return: actions
        """
        @Validate.numeric(WrongOption)
        def wrapper(entry: int):
            number = int(entry)

            queries = (self.query_0, self.query_1, self.query_2,
                       self.query_3, self.query_4, self.query_5,
                       self.query_6, self.wrong_query)

            if 0 <= number <= 6:
                # call certain query
                return queries[number]

            # wrong_query is requested
            else:
                return queries[-1]

        return wrapper(query)

    def run_thread(self):
        """
        Perpetual asking queries until exit
        :return:
        """
        print(self.messages.menu_choices)
        while True:
            entry = input(self.messages.query_input(self.counter))
            try:
                self.process_query(entry)()

            # wrong query
            except WrongOption:
                self.wrong_query()

            # exit demand
            except ImmediateExit:
                return

            # queries counter increment
            else:
                self.counter += 1
