
from bojo.models.Cron_Schedule import CronSchedule
from bojo.models.Daily_Cron_Schedule import DailyCronSchedule
from bojo.models.Monthly_Cron_Schedule import MonthlyCronSchedule
from bojo.models.Weekly_Cron_Schedule import WeeklyCronSchedule
from bojo.types.schedule_types import ScheduleType


class ScheduleFactory:


    @staticmethod
    def getSchedule(type, **kwargs):

        if type == ScheduleType.DAILY.value:
            return DailyCronSchedule(**kwargs)
        
        elif type == ScheduleType.WEEKLY.value:
            return WeeklyCronSchedule(**kwargs)
        
        elif type == ScheduleType.MONTHLY.value:
            return MonthlyCronSchedule(**kwargs)
        #returns a Once schedule
        else:
            return CronSchedule(**kwargs)
