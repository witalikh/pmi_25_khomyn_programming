"""
File for InterfaceMessage class and prepare_messages function
"""

from settings import Globals


class InterfaceMessages:
    """ Class for Interface Messages storing """

    def __init__(self, greeting,
                 menu_choices,
                 vaccine_choices,
                 parameter_choices,

                 all_certificates, matching_certificates,
                 sorted_certificates, appended_certificate,

                 query_input, wrong_query,
                 exit_message,

                 identifier_input, wrong_identifier,
                 search_by_identifier,

                 name_input, wrong_name,
                 passport_input, wrong_passport,

                 birth_date_input, wrong_birth_date_young, wrong_birth_date_old, wrong_birth_date_format,
                 start_date_input, wrong_start_date, wrong_start_date_format,
                 end_date_input, wrong_end_date, wrong_end_date_format,

                 vaccine_input, wrong_vaccine,
                 parameter_input, wrong_parameter,

                 absent_record, identifier_change,
                 entry_input
                 ):
        """
        Initializes InterfaceMessages object for convenience
        """
        self.greeting = greeting

        self.menu_choices = menu_choices
        self.vaccine_choices = vaccine_choices
        self.parameter_choices = parameter_choices

        self.all_certificates = all_certificates
        self.matching_certificates = matching_certificates
        self.sorted_certificates = sorted_certificates
        self.appended_certificate = appended_certificate

        self.query_input = query_input
        self.wrong_query = wrong_query
        self.exit_message = exit_message

        self.identifier_input = identifier_input
        self.wrong_identifier = wrong_identifier
        self.search_by_identifier = search_by_identifier

        self.name_input = name_input
        self.wrong_name = wrong_name

        self.passport_input = passport_input
        self.wrong_passport = wrong_passport

        self.wrong_birth_date_format = wrong_birth_date_format
        self.wrong_start_date_format = wrong_start_date_format
        self.wrong_end_date_format = wrong_end_date_format

        self.birth_date_input = birth_date_input
        self.wrong_birth_date_young = wrong_birth_date_young
        self.wrong_birth_date_old = wrong_birth_date_old

        self.start_date_input = start_date_input
        self.wrong_start_date = wrong_start_date

        self.end_date_input = end_date_input
        self.wrong_end_date = wrong_end_date

        self.vaccine_input = vaccine_input
        self.wrong_vaccine = wrong_vaccine

        self.parameter_input = parameter_input
        self.wrong_parameter = wrong_parameter

        self.absent_record = absent_record
        self.identifier_change = identifier_change
        self.entry_input = entry_input


def prepare_messages():
    """
    Function with prepared ukrainian messages
    :return:
    """

    greeting = "Доброго дня!"

    menu_choices = "0. Вийти з програми. \n" \
                   "1. Надрукувати всі наявні сертифікати в базі даних. \n" \
                   "2. Знайти i надрукувати всі сертифікати, що містять в одному з полів.\n" \
                   "3. Додати запис (міжнародний сертифікат вакцинації від CoViD-19). \n" \
                   "4. Редагувати запис (міжнародний сертифікат вакцинації від CoViD-19). \n" \
                   "5. Видалити запис (міжнародний сертифікат вакцинації від CoViD-19). \n" \
                   "6. Посортувати записи за певним параметром. " \

    parameter_choices = "Введіть один з наступних параметрів власноруч без лапок: \n" \
                        "'id' 'name' 'passport' 'birthday' 'start date' 'end date' 'vaccine'.\n"

    def form_vaccines_list():
        return ", ".join(Globals.available_vaccines) + "\n"

    vaccine_choices = form_vaccines_list()

    all_certificates = "Відображено всі сертифікати в базі даних: \n"

    def matching_certificates(entry: str):
        return f"Відображено всі сертифікати, що містять в хоча б одному з полів {entry}: \n"

    sorted_certificates = "За певним параметром відсортовано сертифікати в базі даних: \n"

    appended_certificate = "Новоутворений сертифікат виглядатиме ось так: \n"

    identifier_input = "Certificate ID (ціле число): "
    wrong_identifier = "Введений Certificate ID є некоректного типу.\n" \
                       "Спробуйте ще раз! \n"
    search_by_identifier = "Введіть Certificate ID для пошуку сертифіката і подальших дій.\n"

    name_input = "Прізвище, ім'я і по-батькові: "
    wrong_name = "Даного ПІБ не може існувати взагалі. Спробуйте ще раз!\n"

    passport_input = "Серія і номер закордонного паспорта (разом): "
    wrong_passport = "Введено некоректний формат серії і номеру закордонного паспорта.\n" \
                     "Спробуйте ще раз! \n"

    birth_date_input = "Дата народження (dd.mm.yyyy): "
    wrong_birth_date_young = "В даному віці ще неможливо отримати закордонний паспорт, і, відповідно, вакцинацію.\n" \
                             "Введіть коректну дату народження, будь-ласка! \n"
    wrong_birth_date_old = "Максимальний зареєстрований вік людини - 122 роки. \n" \
                           "Введіть коректну дату народження або звертайтесь до Книги рекордів Гіннеса!\n"

    wrong_birth_date_format = "Введена Вами дата народження некоректна за форматом.\n" \
                              "Спробуйте ще раз! \n"

    start_date_input = "Дійсний з (dd.mm.yyyy): "
    wrong_start_date = "Дане календарне число в Вашому випадку не може бути датою початку дії сертифікату.\n" \
                       "Спробуйте ще раз!\n"
    wrong_start_date_format = "Введена Вами дата початку дії сертифікату некоректна за форматом.\n" \
                              "Спробуйте ще раз! \n"

    end_date_input = "Дійсний до (dd.mm.yyyy): "
    wrong_end_date = "Дане календарне число в Вашому випадку не може бути кінцевою датою дії сертифікату.\n" \
                     "Спробуйте ще раз!\n"
    wrong_end_date_format = "Введена Вами дата кінця дії сертифікату некоректна за форматом.\n" \
                            "Спробуйте ще раз! \n"

    vaccine_input = "Виберіть вакцину, ввівши її власноруч: \n" + vaccine_choices

    wrong_vaccine = "Даної вакцини не існує або вона не схвалена ВООЗ\n" \
                    "Спробуйте ще раз! \n"

    parameter_input = "Параметр: "
    wrong_parameter = "Такого параметру не існує! \n" \
                      "Спробуйте ще раз! \n"

    absent_record = "Даного запису в реєстрі не виявлено. Жодної дії не виконано.\n"
    identifier_change = "Даний параметр редагувати заборонено! \n"

    entry_input = "Значення, що повинно бути десь в сертифікаті: "

    def query_input(number: int):
        return f"[{number}]: "

    wrong_query = "\nДаний запит некоректний. Будь-ласка, повторіть ще раз!"

    exit_message = "Програма завершує свою роботу. До побачення!"

    return InterfaceMessages(greeting,
                             menu_choices,
                             vaccine_choices,
                             parameter_choices,

                             all_certificates, matching_certificates,
                             sorted_certificates, appended_certificate,

                             query_input, wrong_query,
                             exit_message,

                             identifier_input, wrong_identifier,
                             search_by_identifier,

                             name_input, wrong_name,
                             passport_input, wrong_passport,

                             birth_date_input, wrong_birth_date_young, wrong_birth_date_old, wrong_birth_date_format,
                             start_date_input, wrong_start_date, wrong_start_date_format,
                             end_date_input, wrong_end_date, wrong_end_date_format,

                             vaccine_input, wrong_vaccine,
                             parameter_input, wrong_parameter,

                             absent_record, identifier_change,
                             entry_input)
