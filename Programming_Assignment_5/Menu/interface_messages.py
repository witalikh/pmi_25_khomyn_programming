"""
File for InterfaceMessage class and prepare_messages function
"""

from settings import Globals
from Common.json_manager import JSONManager


class InterfaceMessages:
    """ Class for Interface Messages storing """

    @staticmethod
    def keys():
        keys_tuple = (
            "greeting",
            "menu_choices",
            "parameter_choices",

            "all_certificates",
            "matching_certificates",
            "sorted",
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
            "entry_input",

            "undo_success",
            "redo_success",
            "nothing_to_undo",
            "nothing_to_redo"
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
            setattr(self, key, kwargs.get(key, lorem_ipsum))

    def process_templates(self, template, **kwargs):
        """
        Method of modifying template valued field into something else
        :param template: template to be replaced
        :param kwargs: attribute-value pairs to replace templates
        """
        for key, value in self.items():
            if value == template:
                self.__dict__[key] = kwargs[key]


def prepare_messages():
    """
    Function with prepared ukrainian messages
    :return: InterfaceMessage Object with ukrainian messages
    """

    # generating dynamic strings
    def form_vaccines_list():
        return ", ".join(Globals.available_vaccines) + "\n"

    dynamic_strings = {
        "vaccine_input": "Виберіть вакцину, ввівши її власноруч:\n" + form_vaccines_list()
    }

    # loading messages from file and process dynamic strings
    file_manager = JSONManager("Menu\\lang_uk.json")
    messages = file_manager.extract_info(InterfaceMessages)[0]
    messages.process_templates("@dynamic_string", **dynamic_strings)

    return messages
