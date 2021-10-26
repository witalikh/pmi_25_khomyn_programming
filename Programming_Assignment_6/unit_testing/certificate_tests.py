from unit_testing.assistant import *


class CertificateValidation(TestCase):
    """ Namespace for tests that work with valid samples"""

    def test_validation(self):
        """ Test: all certificates here suppose to be valid """

        try:
            JSONManager(LOCALS.VALID_SAMPLES_PATH).extract_info(CovidCertificate)

        except Exception as e:
            self.fail(msg=f"Unexpected exception raised: {repr(e)}")


class InvalidCasesAnalysis(TestCase):
    """ Namespace for tests that work with invalid samples """

    def test_validation(self):
        """ Test: no certificate should pass """

        certificate_loader = JSONManager(LOCALS.INVALID_SAMPLES_PATH)
        result = certificate_loader.extract_info(CovidCertificate, lambda *args: None)

        if len(result) > 0:
            self.fail(f"None of the certificates supposed to be valid, not {len(result)}")

    def test_invalid(self):
        """ Test: no one should pass only by particular reasons """

        certificate_loader = JSONManager(LOCALS.INVALID_SAMPLES_PATH)

        errors_loader = JSONManager(LOCALS.INVALID_SAMPLES_REASONS_PATH)
        suspected_errors = errors_loader.extract_info()

        counter = 0

        def errors_checker(filename, obj, exception):

            if not isinstance(exception, MultipleCertErrors):
                self.fail(f"Unexpected exception raised: {repr(exception)}")

            else:
                nonlocal counter
                errors_counter = 0

                for error in exception:
                    if error.__class__.__name__ not in suspected_errors[counter]:
                        self.fail(f"Certificate #{counter} from {filename}: \n"
                                  f"Unexpected CertError in MultipleCertErrors: {repr(error)}")
                    else:
                        errors_counter += 1

                else:
                    expected_errors = len(suspected_errors[counter])

                    if errors_counter != expected_errors:
                        self.fail(f"Expected more exceptions in certificate #{counter}: {expected_errors} "
                                  f"instead of {errors_counter}")
                    else:
                        counter += 1

        certificate_loader.extract_info(CovidCertificate, errors_checker)


__all__ = ["CertificateValidation", "InvalidCasesAnalysis"]
