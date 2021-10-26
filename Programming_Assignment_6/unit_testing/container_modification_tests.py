from unit_testing.assistant import *
from operator import attrgetter


class ExtendingTests(TestCase):
    """ Namespace class for testing container append/extend actions"""

    def test_upload_valid(self):
        """ Test: all certificates should be loaded into """

        try:
            quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)

        except Exception as e:
            self.fail(f"Unexpected exception raised: {repr(e)}")

    def test_upload_invalid(self):
        """ Test: no certificates should be loaded into """

        container = Container()
        try:
            uploader = JSONManager(LOCALS.INVALID_SAMPLES_PATH)
            container.extend(uploader.extract_info(dict))
        except TypeError:
            pass

        else:
            self.fail("Expected TypeError while uploading")

        self.assertRaises(TypeError, container.extend, None,
                          msg="Invalid value passed forward or method does not work")

    def test_adding_valid_record(self):
        """ Test: valid sample should be added while invalid shouldn't"""

        container = Container()
        try:
            container.add_record(LOCALS.SAMPLE_OBJ)

        except Exception as e:
            self.fail(f"Unexpected exception raised: {repr(e)}")

    def test_adding_invalid_record(self):
        """ Test: this case should not be added """

        container = Container()
        try:
            container.add_record(None)

        except TypeError:
            pass

        else:
            self.fail(f"Expected TypeError to raise")


class EditTests(TestCase):
    """ Namespace for tests concerning edition the records """

    def test_edit_absent_record(self):
        """ Test: nothing but AbsentError should be raised """

        container = quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)

        try:
            container.edit_record("anonymous", "vaccine", "00000")

        except MultipleCertErrors as multi_errors:
            if CertError.AbsentRecord not in multi_errors:
                self.fail("Expected AbsentRecord in MultipleCertErrors")

        else:
            self.fail("Expected MultipleCertErrors")

    def test_edit_record_wrongly(self):
        """ Test: the record should not be changed """

        container = Container()
        container.add_record(LOCALS.SAMPLE_OBJ)

        try:
            container.edit_record('456', "date_of_birth", "29.02.2001")

        except MultipleCertErrors as multi_errors:
            if CertError.InvalidBirthDateFormat not in multi_errors:
                self.fail("Expected InvalidBirthDateFormat in MultipleCertErrors")

            self.assertEqual(getattr(container[0], "date_of_birth"),
                             LOCALS.SAMPLE_OBJ["date_of_birth"], "Edit did not work")

        else:
            self.fail("Expected MultipleCertErrors")

    def test_edit_record_properly(self):
        """ Test: the record should be changed """

        container = Container()
        container.add_record(LOCALS.SAMPLE_OBJ)

        try:
            container.edit_record("456", "date_of_birth", "29.02.2000")

        except Exception as e:
            self.fail(f"Unexpected exception raised: {repr(e)}")

        else:
            self.assertEqual(str(getattr(container[0], "date_of_birth")),
                             "29.02.2000", "Edit did not work")


class DeletionTests(TestCase):
    """ Namespace for tests concerning deleting some elements """

    def test_delete_absent_record(self):
        """ Test: should raise AbsentRecord """

        container = Container()
        container.add_record(LOCALS.SAMPLE_OBJ)

        try:
            container.delete_record("anonymous")

        except MultipleCertErrors as multi_errors:
            if CertError.AbsentRecord not in multi_errors:
                self.fail("Expected AbsentRecord in MultipleCertErrors")

        else:
            self.fail("Expected MultipleCertErrors")

    def test_delete_existing_record(self):
        """ Test: should raise AbsentRecord """

        container = Container()
        container.add_record(LOCALS.SAMPLE_OBJ)

        try:
            container.delete_record("456")

        except Exception as e:
            self.fail(f"Unexpected exception raised: {repr(e)}")

        else:
            self.assertEqual(len(container), 0,
                             "Deletion did not work")

    def test_clear(self):
        """ Test: container should be empty after """

        container = quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)
        old_size = len(container)

        self.assertTrue(old_size > 0, "Invalid Test Cases: nothing was loaded")

        container.clear()
        self.assertNotEqual(old_size, len(container),
                            "Clean method did not work")


class SortTests(TestCase):
    """ Namespace for sorting certificates tests """

    container = Container()
    container.add_record(LOCALS.SAMPLE_OBJ)

    container = container + quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)

    def test_wrong_parameter(self):
        """ Test: parameter should not be recognized """
        try:
            self.container.sort(key=attrgetter("false_parameter"))
        except AttributeError:
            pass
        else:
            self.fail("Expected AttributeError")

    def test_sorts(self):
        """ Test: every kind of sort should work properly """

        def check_sort(attr, reverse):

            spy_list = [getattr(elem, attr) for elem in self.container]
            spy_list.sort(reverse=reverse)

            try:
                self.container.sort(key=attrgetter(attr), reverse=reverse)

            except Exception as e:
                self.fail(f"Unexpected exception raised: {repr(e)}")

            else:
                for index, element in enumerate(spy_list):
                    if getattr(self.container[index], attr) != element:
                        self.fail(f"Sorting algorithm is not working as expected:\n"
                                  f"Check list: {', '.join(spy_list)};\n"
                                  f"Stuck: index {index}, element - {str(element)}")

        configs = [("date_of_birth", False), ("vaccine", True),
                   ("username", False), ("end_date", True)]

        for config in configs:
            check_sort(*config)


__all__ = ["ExtendingTests", "EditTests", "DeletionTests", "SortTests"]
