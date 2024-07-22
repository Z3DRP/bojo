
class CronSchedule:
    
    def __init__(self, scheduleName:str, day:int, dayOfWeek:int, hour:int, minute:int, everyHour:int, everyMinute:int, durr:float, numberSubmissions:int):
        self.name = scheduleName
        self.durration = durr
        self.numberOfSubmissions = numberSubmissions
        self.dayOfWeek = dayOfWeek
        self.day = day
        self.hour = hour
        self.minute = minute
        self.everyHour = everyHour
        self.everyMinute = everyMinute