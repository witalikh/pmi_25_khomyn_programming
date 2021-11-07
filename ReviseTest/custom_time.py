from validators import Validators


class Time:
    def __init__(self, *args: str):

        if len(args) == 1:
            values = str(args[0]).split(":")
            self.hour = Validators.BetweenMatch(0, 23, int)(values[0])
            self.minute = Validators.BetweenMatch(0, 59, int)(values[1])

    def __lt__(self, other):
        return self.hour < other.hour or \
            self.hour == other.hour and self.minute < other.minute

    def __gt__(self, other):
        return self.hour > other.hour or \
            self.hour == other.hour and self.minute > other.minute

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __ne__(self, other):
        return self.hour != other.hour or self.minute != other.minute

    def __str__(self):
        return str(self.hour)+":"+str(self.minute)
