from copy import deepcopy


class FileManager:
    """
    Class for automatic managing with file writing, reading and clearing
    With behaviour as database managing system
    """

    def __init__(self, filename, encoding="UTF-8", sep=" : "):
        """
        Creating file manager object
        :param filename: file or path to the file
        :param sep: separator between keys and values
        """
        self.filename = filename
        self.encoding = encoding
        self.sep = sep

        self.field_begin = "{"
        self.field_end = "}"

        self.record_begin = f"++ # ++++++++++ # ++\n"
        self.record_end = f"-- # ---------- # --\n"

    def append_info(self, **kwargs):
        """
        Method of appending file with a record
        If file does not exist, it creates it
        :param kwargs: dictionary to append file with
        :return:
        """
        with open(self.filename, mode="at", encoding=self.encoding) as file:
            # write start indicator
            file.write(self.record_begin)

            # unpack kwargs and write accordingly
            for key, value in kwargs.items():
                file.write(str(key) +
                           self.sep + self.field_begin + str(value) + self.field_end +
                           '\n')

            # write end indicator
            file.write(self.record_end)

        return

    def extend_info(self, iterable):
        """
        Method of appending file from
        :param iterable:
        :return:
        """
        # open file for appending
        with open(self.filename, mode="at", encoding=self.encoding) as file:
            for element in iterable:
                # write start indicator
                file.write(self.record_begin)

                # unpack kwargs and write accordingly
                for key, value in element.items():
                    file.write(str(key) +
                               self.sep + self.field_begin + str(value) + self.field_end +
                               '\n')

                # write end indicator
                file.write(self.record_end)

            return

    def clear_info(self):
        """
        Method of cleaning file entirely
        :return:
        """
        # open file in cleaning mode and write newline
        with open(self.filename, mode="wt", encoding=self.encoding) as file:
            file.write("")

        # that's all
        return

    def extract_info(self, cls=None):
        """
        Method of reading all records in the file
        :param cls:
        :return: list of cls objects
        """
        result = []
        try:
            # if file exists, open it
            with open(self.filename, mode="rt", encoding=self.encoding) as file:
                # any number of arguments
                kwargs = {}

                field_key = None
                field_value = ""

                # marker if there's recording to the object
                record_scanning = False
                field_scanning = False

                # scan every line
                for line in file:

                    # indicator of record start
                    if line.startswith("++"):
                        record_scanning = True

                    # indicator of record end when record not corrupted
                    elif line.startswith("--") and record_scanning:

                        # convert to class object if possible
                        if cls is not None:
                            try:
                                result.append(cls(**kwargs))

                            except:
                                pass

                        # no need to convert into class, append with dict
                        else:
                            result.append(deepcopy(kwargs))

                        # record reading is finished
                        kwargs.clear()
                        record_scanning = False

                    # if record scanning is going on
                    elif record_scanning and not field_scanning:
                        try:
                            # preformat strings and write to kwargs
                            stripped = line.strip()
                            key, value = stripped.split(self.sep)

                        # incorrect row found
                        except ValueError:
                            record_scanning = False
                            kwargs.clear()

                        else:
                            if value.startswith(self.field_begin):
                                if not value.endswith(self.field_end):
                                    field_scanning = True
                                    field_key = key
                                    field_value += (value[1:] + '\n')
                                else:
                                    kwargs[key] = value[1:-1]

                    elif record_scanning and field_scanning:
                        if not line.endswith(self.field_end + '\n'):
                            field_value += line
                        else:
                            field_value += line[:-2]
                            kwargs[field_key] = field_value

                            field_scanning = False
                            field_key = None
                            field_value = ""

                    else:
                        continue

        # if file not found, nothing to do
        except FileNotFoundError:
            pass

        finally:
            # return iterable of dicts or objects
            return result
