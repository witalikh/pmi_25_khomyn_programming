"""
File for InterfaceMessage class and prepare_messages function
"""

from settings import Globals
from common.json_manager import JSONManager


class InterfaceMessages:
    """ Class for Interface Messages storing """

    def __init__(self, **kwargs):
        """ Initializer: """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, item):
        """ Get attribute like in a dictionary """
        return getattr(self, item, "lorem ipsum")

    def preprocess(self, template, **kwargs):
        """
        Method of modifying template valued field into something else
        :param template: template to be replaced
        :param kwargs: attribute-value pairs to replace templates
        """
        for key, value in kwargs.items():
            setattr(self, key, getattr(self, key).replace(template, value))


def prepare_messages(filename: str):
    """
    Function with prepared ukrainian messages
    :return: InterfaceMessage Object with ukrainian messages
    """

    dynamic_strings = {
        "vaccine_input": ", ".join(Globals.available_vaccines) + "\n"
    }

    # loading messages from file and process dynamic strings
    file_manager = JSONManager(filename)
    messages = file_manager.extract_info(InterfaceMessages)[0]
    messages.preprocess("{vaccines}", **dynamic_strings)

    return messages
