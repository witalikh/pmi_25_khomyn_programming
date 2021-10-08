"""
File for InterfaceMessage class and prepare_messages function
"""

from settings import Globals
from file_manager import FileManager


class InterfaceMessages:
    """ Class for Interface Messages storing """

    @staticmethod
    def keys():
        keys_tuple = (
            "greeting",
            "menu_choices",
            "vaccine_choices",
            "parameter_choices",

            "all_certificates",
            "matching_certificates",
            "sorted_certificates",
            "appended_certificate",

            "query_input",
            "wrong_query",
            "exit_message",

            "identifier_input",
            "wrong_identifier",
            "search_by_identifier",

            "name_input",
            "wrong_name",
            "passport_input",
            "wrong_passport",

            "birth_date_input",
            "wrong_birth_date_young",
            "wrong_birth_date_old",
            "wrong_birth_date_format",
            "start_date_input",
            "wrong_start_date",
            "wrong_start_date_format",
            "end_date_input",
            "wrong_end_date",
            "wrong_end_date_format",

            "vaccine_input",
            "wrong_vaccine",
            "parameter_input",
            "wrong_parameter",

            "absent_record",
            "identifier_change",
            "entry_input"
        )

        return keys_tuple

    def items(self):
        return [(key, self.__dict__[key]) for key in self.keys()]

    def values(self):
        return [self.__dict__[key] for key in self.keys()]

    def __init__(self, **kwargs):
        """
        Initializes InterfaceMessages object for convenience
        """
        lorem_ipsum = "lorem ipsum"

        for key in InterfaceMessages.keys():
            self.__dict__[key] = kwargs.get(key, lorem_ipsum)

    def process_templates(self, template, **kwargs):
        for key, value in self.items():
            if value == template:
                self.__dict__[key] = kwargs[key]


def prepare_messages():
    """
    Function with prepared ukrainian messages
    :return:
    """

    def form_vaccines_list():
        return ", ".join(Globals.available_vaccines) + "\n"

    def matching_certificates(entry: str):
        return f"Відображено всі сертифікати, що містять в хоча б одному з полів {entry}: \n"

    def query_input(number: int):
        return f"[{number}]: "

    dynamic_strings = {
        "vaccine_choices": form_vaccines_list(),
        "matching_certificates": matching_certificates,
        "query_input": query_input,
        "vaccine_input": "Виберіть вакцину, ввівши її власноруч:\n" + form_vaccines_list()
    }

    strings_file_manager = FileManager("lang_uk.txt")
    messages = (strings_file_manager.extract_info(InterfaceMessages))[0]
    messages.process_templates("@dynamic_string", **dynamic_strings)

    return messages
