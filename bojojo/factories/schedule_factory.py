
from bojojo.models.Cron_Schedule import CronSchedule
from bojojo.models.Daily_Cron_Schedule import DailyCronSchedule
from bojojo.models.Monthly_Cron_Schedule import MonthlyCronSchedule
from bojojo.models.Weekly_Cron_Schedule import WeeklyCronSchedule
from bojojo.types.schedule_types import ScheduleType


class ScheduleFactory:


    @staticmethod
    def getSchedule(type, **kwargs):

        if type.upper() == ScheduleType.DAILY.name:
            return DailyCronSchedule(**kwargs)
        
        elif type.upper() == ScheduleType.WEEKLY.name:
            return WeeklyCronSchedule(**kwargs)
        
        elif type.upper() == ScheduleType.MONTHLY.name:
            return MonthlyCronSchedule(**kwargs)
        
        else:
            return CronSchedule(**kwargs)
