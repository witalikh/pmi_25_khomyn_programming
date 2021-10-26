"""
File for processing queries with CovidCertificates
"""
from CovidCertificate.certificate import CovidCertificate
from CovidCertificate.container import Container
from CovidCertificate.certificate_validation import MultipleCertErrors

from Memento.memento import CareTaker, NothingToUndo, NothingToRedo

from Common.json_manager import JSONManager
from Common.validators import Validate

from Menu.input_manager import InputManager
from Menu.interface_messages import InterfaceMessages

from operator import attrgetter


class ImmediateExit(Exception):
    """ Class for force exit """
    pass


class WrongOption(Exception):
    """ Class for wrong option """
    pass


class CertificatesQueriesThread:
    """ Class responsible for managing sequent queries """

    def __init__(self, database, messages: InterfaceMessages):
        """
        Initialize
        :param database: file which serves as CoViD-19 certificates database
        :param messages: object of class with strings for menu
        """
        # container and its caretaker
        self.container = Container()
        self.caretaker = CareTaker(self.container, CovidCertificate)

        # managers
        self.file_manager = JSONManager(database)
        self.input_manager = InputManager(messages)

        # messages
        self.messages = messages
        self.counter = 0

        # load database before start
        self.load_database()

    def load_database(self):
        """
        Extract data from file into container and update file from errors
        """
        result = self.file_manager.extract_info(CovidCertificate,
                                                exception_handler=self.input_manager.log_errors)
        self.container.extend(result)
        self.update_database()
        return

    def update_database(self):
        """
        Update file records
        """
        self.file_manager.rewrite_info(self.container)
        return

    @property
    def caretaker_state(self):
        """
        How many undo and redo available
        """
        return {
            "undo_available": self.caretaker.undo_count,
            "redo_available": self.caretaker.redo_count
        }

    def query_0(self):
        """
        Exit
        """
        print(self.messages.exit_message)
        raise ImmediateExit

    def query_1(self):
        """
        Print all certificates
        """
        print(self.messages.all_certificates)
        for certificate in self.container:
            print(certificate)

        return

    def query_2(self):
        """
        Find all possible matches and print
        """
        # ask for value to find all matches
        entry = input(self.messages.entry_input)
        result = self.container.find_all(entry)

        # print all matches
        print(self.messages.matching_certificates.format(entry=entry))
        for certificate in result:
            print(certificate)

        return

    def query_3(self):
        """
        Input certificate manually and write it to file
        """
        # save memento in caretaker and try to input certificate
        self.caretaker.snapshot_before_change()
        certificate = self.input_manager.input_certificate()

        # valid certificate entered
        if certificate:
            # append container
            self.container.add_record(certificate)

            # update the database
            self.caretaker.accept_change()
            self.update_database()

            # update database and caretaker
            print(self.messages.appended_certificate)
            print(certificate)
        else:
            # nothing changed, delete memento from caretaker
            self.caretaker.decline_change()

        return

    def query_4(self):
        """
        Edit the record in according place and rewrite the file
        """

        # ask for valid identifier and parameter
        identifier = self.input_manager.input_identifier()
        parameter = self.input_manager.input_parameter()

        # invalid parameter name
        if parameter is None:
            return

        # forbidden parameter to edit
        elif parameter == "identifier":
            print(self.messages.identifier_change)
            return

        else:
            # save memento in caretaker and ask value
            self.caretaker.snapshot_before_change()
            value = input(self.input_manager.get_message_from_parameter(parameter))

            try:
                # try to edit the record
                self.container.edit_record(identifier, parameter, value)

            except MultipleCertErrors as instances:
                # nothing changed, delete memento from caretaker
                self.caretaker.decline_change()

                # print all exceptions
                for instance in instances:
                    print(self.input_manager.get_exception_message(instance))
                return

            else:
                # update database and caretaker
                self.caretaker.accept_change()
                self.update_database()
                return

    def query_5(self):
        """
        Delete the record from container
        """
        # save memento in caretaker and ask id
        self.caretaker.snapshot_before_change()
        identifier = self.input_manager.input_identifier()

        try:
            # delete if record exists
            self.container.delete_record(identifier)

        except MultipleCertErrors as instances:
            # nothing changed, delete memento from caretaker
            self.caretaker.decline_change()

            # print all exceptions
            for instance in instances:
                print(self.input_manager.get_exception_message(instance))
            return

        else:
            # update database and caretaker
            self.caretaker.accept_change()
            self.update_database()
            return

    def query_6(self):
        """
        Sort container by parameter and show it
        :return:
        """
        # save memento in caretaker and ask parameter
        self.caretaker.snapshot_before_change()
        parameter = self.input_manager.input_parameter()

        if parameter is not None:
            # sort by parameter if got parameter
            print(self.messages.sorted)
            self.container.sort(key=attrgetter(parameter))

            # update database and caretaker
            self.caretaker.accept_change()
            self.update_database()
            return

        else:
            # nothing changed, delete memento from caretaker
            self.caretaker.decline_change()
            return

    def query_7(self):
        """ Undo """
        try:
            self.caretaker.undo()

        except NothingToUndo:
            print(self.messages.nothing_to_undo)
            return

        else:
            print(self.messages.undo_success.format(**self.caretaker_state))
            self.update_database()
            return

    def query_8(self):
        """ Redo """
        try:
            self.caretaker.redo()

        except NothingToRedo:
            print(self.messages.nothing_to_redo)
            return

        else:
            print(self.messages.redo_success.format(**self.caretaker_state))
            self.update_database()
            return

    def wrong_query(self):
        """
        User entered wrong query, warn him about it
        """
        print(self.messages.wrong_query)
        print()
        print(self.messages.menu_choices.format(**self.caretaker_state))

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
                       self.query_6, self.query_7, self.query_8,
                       self.wrong_query)

            if 0 <= number < len(queries) - 1:
                # call certain query
                return queries[number]

            # wrong_query is requested
            else:
                return queries[-1]

        return wrapper(query)

    def run_thread(self):
        """
        Perpetual asking queries until exit
        """
        print(self.messages.menu_choices.format(**self.caretaker_state))
        while True:
            entry = input(self.messages.query_input.format(number=self.counter))
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
