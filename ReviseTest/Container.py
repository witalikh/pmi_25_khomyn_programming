from FlightBooking import FlightBooking, BookingException


class ContainerException(Exception):

    def __init__(self, msg):
        self.msg = msg


class Container:

    def __init__(self):
        self._container = []

    def __len__(self):
        return len(self._container)

    def __iter__(self):
        return iter(self._container)

    def __getitem__(self, item):
        return self._container[item]

    def _validate_new_entry(self, entry: FlightBooking):
        if not isinstance(entry, FlightBooking):
            raise TypeError

        else:
            avia = entry["avia_company"]
            flight = entry["flight_number"]
            date = entry["date"]
            start_time = entry["start_time"]
            end_time = entry["end_time"]

            for instance in self._container:
                if instance["flight_number"] == flight and\
                        instance["avia_company"] == avia and\
                        instance["date"] == date:

                    if instance["end_time"] > start_time and end_time > instance["start_time"]:
                        raise ContainerException(msg="Flight overlaps")

    def append(self, instance: FlightBooking):
        self._validate_new_entry(instance)

        self._container.append(instance)

    def clear(self):
        self._container.clear()

    def get_sorted(self, reverse=False, key=None):
        sorted_container = sorted(self._container, reverse=reverse, key=key)

        new_instance = Container()
        new_instance._container = sorted_container
        return new_instance
