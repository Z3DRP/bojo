
from bojo.models.Cron_Schedule import CronSchedule


class DailyCronSchedule(CronSchedule):
    
    def __init__(self, name:str, dayOfWeek:str, hour:int, minute:int, everyHour:int, everyMinute:int, durr:float, numberSubmissions:int):
        super().__init__(name, dayOfWeek, hour=hour, minute=minute, everyHour=everyHour, everyMinute=everyMinute, durr=durr, numberSubmissions=numberSubmissions)
        self.daily = True
