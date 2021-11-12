from unit_testing.assistant import *


class InfoExtractTests(TestCase):
    """ Namespace for tests checking non-modifying methods """

    FIND_AA_RESULTS_PATH = "certificates/find_all_aa.json"
    FIND_DOE_RESULTS_PATH = "certificates/find_all_Doe.json"

    def test_find_all(self):
        """ Test: it should find any matching ever in all container """

        container = quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)

        def check_method(entry: str, expected_result_source):

            expected_results: Container

            if isinstance(expected_result_source, str):
                expected_results = quick_multiple_load(expected_result_source)

            elif isinstance(expected_result_source, Container):
                expected_results = expected_result_source

            else:
                self.fail("Test Case is not so universal yet")

            matches = container.find_all(entry)

            self.assertEqual(len(expected_results), len(matches),
                             "Actual and expected container sizes mismatching")

            for entry in matches:
                self.assertTrue(entry in expected_results,
                                "Unexpected certificate found")

        configs = [("aa", self.FIND_AA_RESULTS_PATH), (".", container),
                   ("@impossible@", Container()), ("Doe", self.FIND_DOE_RESULTS_PATH)]

        for config in configs:
            check_method(*config)

    def test_iter(self):
        """ Test: iteration should work properly """
        container = quick_multiple_load(LOCALS.VALID_SAMPLES_PATH)
        another_container = Container()

        for cert in container:
            another_container.add_record(cert)

        self.assertEqual(len(container), len(another_container),
                         "Failed find_all() method: actual and expected container sizes mismatch")

        for entry in another_container:
            self.assertTrue(entry in container, "Unexpected certificate found")


__all__ = ["InfoExtractTests"]
