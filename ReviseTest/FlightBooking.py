from AviaCompanies import  AviaCompanies
from validators import Validators, ValidationError
from custom_time import Time


class BookingException(Exception):

    def __init__(self, _dict: dict):
        self.errors = _dict


class FlightBooking:

    @staticmethod
    def keys():
        return [
            "avia_company",
            "number_of_people",
            "start_time",
            "end_time",
            "date",
            "flight_number"
        ]

    @staticmethod
    def validator(key: str):
        validators = {
            "avia_company": Validators.BelongMatch(AviaCompanies.__members__),
            "number_of_people": Validators.BetweenMatch(1, 300, int),
            "start_time": Validators.TypeMatch(Time),  # already validates
            "end_time": Validators.TypeMatch(Time),
            "date": Validators.is_date,
            "flight_number": Validators.PatternMatch(r"[a-zA-Z]{2}\d{4}")
        }
        return validators[key]

    @staticmethod
    def messages_for_invalid(key: str):
        messages = {
            "avia_company": "Invalid avia company chosen",
            "number_of_people": "Invalid number of people onboard",
            "start_time": "Invalid start time",
            "end_time": "Invalid end time",
            "date": "Invalid date format or value",
            "flight_number": "Invalid flight number format"
        }
        return messages[key]

    def __init__(self, **kwargs):

        errors = {}

        for key, value in kwargs.items():
            if key not in self.keys():
                raise AttributeError

            try:
                validated_value = self.validator(key)(value)

            except ValidationError:
                errors[key] = self.messages_for_invalid(key)

            else:
                setattr(self, key, validated_value)

        else:
            if errors:
                raise BookingException(errors)

            else:
                self._validate_dependent(errors)

                if errors:
                    raise BookingException(errors)

    def _validate_dependent(self, _errors):

        local_errors = {
            "end_time": "End time cannot be earlier than start time!"
        }

        try:
            Validators.BetweenMatch(getattr(self, "start_time"), None, Time)(getattr(self, "end_time"))
        except ValidationError:
            _errors["end_time"] = local_errors["end_time"]

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        result = ""
        for key in self.keys():
            result += (key + ": " + str(getattr(self, key)) + "\n")
        return result
