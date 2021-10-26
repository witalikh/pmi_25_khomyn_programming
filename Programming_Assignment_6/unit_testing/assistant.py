from unittest import TestCase

from CovidCertificate import CovidCertificate, Container, MultipleCertErrors, CertError
from common import JSONManager


class LOCALS:
    """ Class for vars common for unit_testing files"""

    SAMPLE_OBJ = CovidCertificate(
        identifier="456",
        username="Seong Gi-hun",
        international_passport="KO456456",
        date_of_birth="01.01.1970",
        start_date="01.01.2021",
        end_date="01.01.2022",
        vaccine="AstraZeneca"
    )

    VALID_SAMPLES_PATH = "certificates/valid_samples.json"

    INVALID_SAMPLES_PATH = "certificates/invalid_samples.json"
    INVALID_SAMPLES_REASONS_PATH = "certificates/invalid_samples_reasons.json"


def quick_multiple_load(path):
    """ """
    container = Container()
    uploader = JSONManager(path)
    container.extend(uploader.extract_info(CovidCertificate))
    return container
