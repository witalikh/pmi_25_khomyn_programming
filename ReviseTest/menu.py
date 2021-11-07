from FlightBooking import FlightBooking, BookingException
from Container import Container, ContainerException
from validators import Validators
from json_handler import read_from_json, write_into_json

from operator import attrgetter


class ImmediateExit(Exception):
    pass


class NoMigrationException(Exception):
    pass


class Menu:

    @staticmethod
    def menu_message(key: str):
        messages = {
            "exit": "Bye!",
            "choices": "0. Exit. \n"
                       "1. Choose file to work with. \n"
                       "2. Print all flight booking records. \n"
                       "3. Add a new flight booking record. \n"
                       "4. Find the most busiest hours from records. \n"
                       "5. Output most busiest airline records. \n",

            "no_migration": "Please choose option 1 and enter file to work with! ",
            "bad_migration": "File contains incorrect data, cannot import! ",
            "no_query": "Wrong query! ",

            "filename": "Input filename: ",
            "no_filename": "Filename is wrong!",

            "avia_company": "Input AviaCompany: ",
            "number_of_people": "Input number of people onboard: ",
            "start_time": "Input start time of flight (hh:mm): ",
            "end_time": "Input end time of flight (hh:mm): ",
            "date": "Input date of flight (yyyy-mm-dd): ",
            "flight_number": "Input flight number (xxYYYY): "
        }
        return messages[key]

    def __init__(self):

        self.filename = None
        self.container: Container = Container()

    def _update_file(self):
        if self.filename is None:
            raise NoMigrationException
        else:
            write_into_json(self.filename, self.container)

    def option_0(self):
        print(self.menu_message("exit"))
        raise ImmediateExit

    def option_1(self):
        filename = input(self.menu_message("filename"))
        try:
            Validators.is_filename(filename)
        except FileNotFoundError:
            print(self.menu_message("no_filename"))
        else:

            self.container.clear()

            try:
                read_from_json(filename, self.container, FlightBooking)
            except (ContainerException, BookingException):
                print(self.menu_message("bad_migration"))

                self.container.clear()
                if self.filename is not None:
                    read_from_json(self.filename, self.container, FlightBooking)
            else:
                self.filename = filename

    def option_2(self):
        for instance in self.container:
            print(instance)

    def option_3(self):
        if self.filename is None:
            raise NoMigrationException

        else:
            params = {}
            for key in FlightBooking.keys():
                params[key] = input(self.menu_message(key))

            try:
                instance = FlightBooking(**params)
                self.container.append(instance)

            except BookingException as exc:
                for value in exc.errors.values():
                    print(value)

            except ContainerException as exc:
                print(exc.msg)

            else:
                self._update_file()

    def option_4(self):
        if self.filename is None:
            raise NoMigrationException
        else:
            sorted_container = self.container.get_sorted(key=attrgetter("start_time"))

            result = {}

            for instance in sorted_container:
                if instance["start_time"].hour not in result.keys():
                    result[instance["start_time"].hour] = 1
                else:
                    result[instance["start_time"].hour] += 1

            max_hour_value = max(result.values())

            print("The most busiest hours are: ")
            for key, value in result.items():
                if value == max_hour_value:
                    print(key, end=" ")
            else:
                print()

    def option_5(self):
        if self.filename is None:
            raise NoMigrationException
        else:
            sorted_container = self.container.get_sorted(key=attrgetter("avia_company"))

            result = {}

            for instance in sorted_container:
                if instance["avia_company"] not in result.keys():
                    result[instance["avia_company"]] = 1
                else:
                    result[instance["avia_company"]] += 1

            max_flights_value = max(result.values())
            busiest = {}

            for key, value in result.items():
                if value == max_flights_value:
                    busiest[key] = []

            for instance in self.container:
                if instance.avia_company in busiest:
                    busiest[instance.avia_company].append(instance)

            for company, flights in busiest.items():
                write_into_json(f"{company}.json", flights)

            print("Successfully outputted busiest airlines!")

    def run_menu(self):
        queries = {
            "0": self.option_0,
            "1": self.option_1,
            "2": self.option_2,
            "3": self.option_3,
            "4": self.option_4,
            "5": self.option_5
        }

        counter = 0

        print(f"Working filename: {self.filename}")
        print(self.menu_message("choices"))
        while True:
            try:
                query = input(f"[{counter}]: ")
                if query in queries.keys():
                    queries[query]()
                else:
                    print(self.menu_message("no_query"))
                    print(f"Filename: {self.filename}")
                    print(self.menu_message("choices"))
            except ImmediateExit:
                break

            except NoMigrationException:
                print(self.menu_message("no_migration"))

            else:
                counter += 1
