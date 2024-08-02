from enum import Enum

class Months(Enum):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUG = 8
    SEPT = 9
    OCT = 10
    NOV = 11
    DEC = 12


def get_month_str(month:Months) -> str:
    if month == Months.JAN:
        return "January"
    elif month == Months.FEB:
        return "Febuary"
    elif month == Months.MAR:
        return "March"
    elif month == Months.APR:
        return "April"
    elif month == Months.MAY:
        return "May"
    elif month == Months.JUNE:
        return "June"
    elif month == Months.JULY:
        return "July"
    elif month == Months.AUG:
        return "August"
    elif month == Months.SEPT:
        return "September"
    elif month == Months.OCT:
        return "October"
    elif month == Months.NOV:
        return "November"
    elif month == Months.DEC:
        return "December"