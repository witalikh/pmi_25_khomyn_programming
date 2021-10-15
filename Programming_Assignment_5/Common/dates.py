"""
File containing own written Date class
"""
# for getting today's date
from datetime import date as system_date


class InvalidDate(Exception):
    """ There is no such date """
    pass


class Date:
    """ Class for date representation """

    @staticmethod
    def days_in_month(month, year):
        """
        Static method of getting number of days in the month
        :param month: number of month
        :param year: number of year
        :return:
        """
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31

        elif month in (4, 6, 9, 11):
            return 30

        elif month == 2:
            leap_year = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
            if leap_year:
                return 29
            else:
                return 28
        else:
            raise InvalidDate(f"There is no such month as {month}")

    @staticmethod
    def name_of_month(order):
        """
        Static method returning English names of months
        :param order: number of month
        :return: name of month
        """
        assert 1 <= order <= 12

        months = ("January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December")

        return months[order - 1]

    def __init__(self, day, month, year, recalculate=False):
        """
        Initializing date object
        :param day: day of the month
        :param month: month of the year
        :param year: year
        :param recalculate: if incorrect day, month or year need to reevaluate
        """
        self.day = day
        self.month = month
        self.year = year

        self.leap_year = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

        # checking data for validity
        self.__validate_date__(recalculate)

    def __validate_date__(self, recalculate=False):
        """
        Private method of validating input date
        :param recalculate: if validation is the part of recalculation
        :return: None or exception if invalid
        """

        # functions to compact the code
        # reevaluation functions
        def days_in_months():
            """ Days are in the current month of year """
            return Date.days_in_month(self.month, self.year)

        def recalculate_month():
            """ Recalculating month of year"""
            # borrow months from previous year
            while self.month <= 0:
                self.month += 12
                self.year -= 1

            # grant months into next year
            while self.month > 12:
                self.month -= 12
                self.year += 1

        def recalculate_day():
            """ Recalculating days until correct """
            # "borrow" days from previous month
            while self.day <= 0:
                self.month -= 1
                recalculate_month()
                self.day += days_in_months()

            # "chew" exceed days into months
            while self.day > days_in_months():
                self.day -= days_in_months()
                self.month += 1
                recalculate_month()

        # negative or zero-value year are considered as BC years (0 is first BC!)
        # for convenience

        # checking month
        if recalculate:
            # arithmetically revalidate the date (for addition and subtraction)
            recalculate_month()

        elif self.month <= 0 or self.month > 12:
            raise InvalidDate(f"{self.month} cannot be a number of month")

        # checking day
        if recalculate:
            recalculate_day()

        elif self.day <= 0 or self.day > days_in_months():
            raise InvalidDate(f"{self.day} can't be a day number in this case")

        # all is valid, return
        return

    def __str__(self):
        """
        Convert Date object into string
        :return: string in format dd.mm.year
        """
        # strings of trouble values
        day_str = str(self.day)
        month_str = str(self.month)

        # if day is one-digit, write zero before
        if self.day < 10:
            day_str = '0' + str(self.day)

        # if month is one-digit, write zero before
        if self.month < 10:
            month_str = '0' + str(self.month)

        return f"{day_str}.{month_str}.{self.year}"

    def __lt__(self, other):
        """
        (<) Compares date with other if other happened later
        :param other: other Date object
        :return: True / False
        """

        return (self.year < other.year) or \
               ((self.year == other.year) and (self.month < other.month or
                                               self.month == other.month and self.day < other.day))

    def __le__(self, other):
        """
        (<=) Compares date with other if other happened not earlier
        :param other: other Date object
        :return: True / False
        """

        return (self.year < other.year) or \
               ((self.year == other.year) and (self.month < other.month or
                                               self.month == other.month and self.day <= other.day))

    def __gt__(self, other):
        """
        (>) Compares date with other if other happened earlier
        :param other: other Date object
        :return: True / False
        """

        return (self.year > other.year) or \
               ((self.year == other.year) and (self.month > other.month or
                                               self.month == other.month and self.day > other.day))

    def __ge__(self, other):
        """
        (>=) Compares date with other if other happened not later
        :param other: other Date object
        :return: True / False
        """

        return (self.year > other.year) or \
               ((self.year == other.year) and (self.month > other.month or
                                               self.month == other.month and self.day >= other.day))

    def __eq__(self, other):
        """
        (==) Compares date with other if other is the same
        :param other: other Date object
        :return: True / False
        """

        return self.year == other.year and self.month == other.month and self.day == other.day

    def __ne__(self, other):
        """
        (!=) Compares date with other if other is not the same
        :param other: other Date object
        :return: True / False
        """

        return self.year != other.year or self.month != other.month or self.day != other.day

    def add(self, days=0, months=0, years=0):
        """
        Makes future date in certain number of days, months or years
        :param days: days to add to this date
        :param months: months to add to this date
        :param years: years to add to this date
        :return: result date
        """
        return Date(self.day + days, self.month + months, self.year + years, True)

    def subtract(self, days=0, months=0, years=0):
        """
        Makes a date in the past in certain number of days, months or years
        :param days: days to add to date
        :param months: months to add to date
        :param years: years to add to date
        :return: result date
        """
        return Date(self.day - days, self.month - months, self.year - years, True)


def get_today_date():
    """
    Gets today's date
    :return: Date object of today's date
    """

    # inventing bicycle?!
    today_date = system_date.today()
    return Date(today_date.day, today_date.month, today_date.year)
