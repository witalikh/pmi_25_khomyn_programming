"""
File containing JSON file manager
"""
import json
import os


class JSONManager:
    """
    Class for automatic managing with file writing, reading and clearing
    With behaviour as database managing system
    """

    def __init__(self, filename, default_converter=dict, encoding="UTF-8", indent: int = 4):
        """
        Creating file manager object
        :param filename: file or path to the file
        :param default_converter: default way to convert object into dict of defaults
        :param encoding: encoding used for reading and writing
        :param indent: separator between keys and values
        """
        self._filename = filename

        self._encoding = encoding
        self._default_converter = default_converter
        self._indent = indent

    def extend_info(self, iterable):
        """
        Method of appending file from iterable
        :param iterable:
        """
        data = []

        # open file for appending
        if os.path.isfile(self._filename):
            with open(self._filename, mode="rt", encoding=self._encoding) as file:
                data = json.load(file)

        for element in iterable:
            data.append(self._default_converter(element))

        with open(self._filename, mode="wt", encoding=self._encoding) as file:
            json.dump(data, file, ensure_ascii=False, indent=self._indent, default=str)

        return

    def clear_info(self):
        """ Cleaning file entirely """
        with open(self._filename, mode="wt", encoding=self._encoding) as file:
            json.dump([], file, ensure_ascii=False, indent=self._indent, default=str)
        return

    def rewrite_info(self, iterable):

        data = []
        for element in iterable:
            data.append(self._default_converter(element))

        with open(self._filename, mode="wt", encoding=self._encoding) as file:
            json.dump(data, file, ensure_ascii=False, indent=self._indent, default=str)

    def extract_info(self, cls=dict, exception_handler=None):
        """
        Method of reading all records in the file
        :param cls: type to convert objects into
        :param exception_handler: function that handles with all possible exceptions
               (params: filename, obj: dict, exception: Exception)
        :return: list of cls objects
        """
        result = []

        try:
            # read every entry in file
            with open(self._filename, mode="rt", encoding=self._encoding) as file:
                data = json.load(file)

                # convert every dictionary into cls object
                for element in data:
                    if cls != dict:
                        try:
                            obj = cls(**element)
                        except Exception as e:
                            if exception_handler is None:
                                raise e
                            else:
                                exception_handler(self._filename, element, e)

                        else:
                            result.append(obj)

                    else:
                        result.append(element)

        except FileNotFoundError:
            with open(self._filename, mode="wt", encoding=self._encoding) as file:
                json.dump([], file, ensure_ascii=False, indent=self._indent, default=str)

        return result
