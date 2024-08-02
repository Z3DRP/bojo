from enum import Enum

class WeekDays(Enum):
    MON = "monday"
    TUE = "tuesday"
    WEN = "wednesday"
    THUR = "thursday"
    FRI = "friday"
    SAT = "saturday"
    SUN = "sunday"


def get_weekday_int(day:WeekDays) -> int:
    if day == WeekDays.MON:
        return 1
    elif day == WeekDays.TUE:
        return 2
    elif day == WeekDays.WEN:
        return 3
    elif day == WeekDays.THUR:
        return 4
    elif day == WeekDays.FRI:
        return 5
    elif day == WeekDays.SAT:
        return 6
    else:
        return 0


def get_weekday(day:int) -> str:
    if day == 0:
        return "Sunday"
    elif day == 1:
        return "Monday"
    elif day == 2:
        return "Tuesday"
    elif day == 3:
        return "Wednesday"
    elif day == 4:
        return "Thursday"
    elif day == 5:
        return "Friday"
    elif day == 6:
        return "Saturday"
