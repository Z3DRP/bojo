from bojojo.types.days import WeekDays
from bojojo.types.months import Months
from bojojo.types.schedule_types import ScheduleType


class RunDate:
    def __init__(self, monthDay:int, weekDay:WeekDays, month:Months, hour:int, minute:int, everyHr:int, everyMin:int, schedType=ScheduleType) -> None:
        self.day_of_month = monthDay
        self.day_of_week:WeekDays = weekDay
        self.month:Months = month
        self.hour = hour
        self.minute = minute
        self.everyHour = everyHr
        self.everyMin = everyMin
        self.runType:ScheduleType = schedType


    @classmethod
    def create_daily(cls, hour:int, minute:int, everyHr:int, everyMin:int):
        return cls(
            monthDay=None,
            weekDay=None,
            month=None, 
            hour=hour, 
            minute=minute, 
            everyHr=everyHr, 
            everyMin=everyMin,
            runType=ScheduleType.DAILY
        )
    

    @classmethod
    def create_weekly(cls, weekDay:ScheduleType, hour:int, minute:int, everyHr:int, everyMin:int):
        return cls(
            monthDay=None, 
            weekDay=weekDay, 
            month=None, 
            hour=hour, 
            minute=minute, 
            everyHr=everyHr, 
            everyMin=everyMin,
            runType=ScheduleType.WEEKLY
        )