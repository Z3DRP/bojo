
class CronSchedule:
    
    def __init__(self, scheduleName:str, dayOfWeek:str, month:str, dayOfMonth:int, hour:int, minute:int, daily:bool, everyHour:int, everyMinute:int):
        self.name = scheduleName
        self.dayOfWeek = dayOfWeek
        self.month = month
        self.dayOfMonth = dayOfMonth
        self.hour = hour
        self.minute = minute
        self.dialy = daily
        self.everyHour = everyHour
        self.everyMinute = everyMinute