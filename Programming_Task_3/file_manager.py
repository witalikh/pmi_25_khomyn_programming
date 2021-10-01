class FileManager:
    """
    Class for automatic managing with file writing, reading and clearing
    With behaviour as database managing system
    """

    def __init__(self, filename, sep=" : "):
        """
        Creating file manager object
        :param filename: file or path to the file
        :param sep: separator between keys and values
        """
        self.filename = filename
        self.sep = sep

        self.record_begin = f"++ # ++++++++++ # ++\n"
        self.record_end = f"-- # ---------- # --\n"

    def append_info(self, **kwargs):
        """
        Method of appending file with a record
        If file does not exist, it creates it
        :param kwargs: dictionary to append file with
        :return:
        """
        with open(self.filename, mode="at") as file:
            # write start indicator
            file.write(self.record_begin)

            # unpack kwargs and write accordingly
            for key, value in kwargs.items():
                file.write(str(key) + self.sep + str(value) + '\n')

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
        with open(self.filename, mode="at") as file:

            # scan every iterable element
            for element in iterable:
                # write start indicator
                file.write(self.record_begin)

                # unpack complex element and write keyword arguments
                for key, value in element.items():
                    file.write(str(key) + self.sep + str(value) + '\n')

                # write end indicator
                file.write(self.record_end)

        return

    def clean_info(self):
        """
        Method of cleaning file entirely
        :return:
        """
        # open file in cleaning mode and write newline
        with open(self.filename, mode="wt") as file:
            file.write("\n")

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
            with open(self.filename, mode="rt") as file:
                # any number of arguments
                kwargs = {}
                # marker if there's recording to the object
                scanning = False

                # scan every line
                for line in file:

                    # indicator of record start
                    if line.startswith("++"):
                        scanning = True

                    # indicator of record end when record not corrupted
                    elif line.startswith("--") and scanning:
                        # convert to class object if possible
                        if cls is not None:
                            # sometimes it impossible to convert
                            try:
                                result.append(cls(**kwargs))

                            # so let pass it out
                            except:
                                pass
                        else:
                            result.append(kwargs)

                        # record reading is finished
                        kwargs.clear()
                        scanning = False

                    # if record scanning is going on
                    elif scanning:
                        try:
                            # preformat strings and write to kwargs
                            stripped = line.strip()
                            key, value = stripped.split(self.sep)
                            kwargs[key] = value

                        # incorrect row found
                        except ValueError:
                            scanning = False
                            kwargs.clear()

                    else:
                        continue

        # if file not found, nothing to do
        except FileNotFoundError:
            pass

        finally:
            # return iterable of dicts or objects
            return result
