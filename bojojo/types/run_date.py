class RunDate:
    def __init__(self, monthDay:int, weekDay:int, month:int, hour:int, minute:int, everyHr:int, everyMin:int, repeat=True) -> None:
        self.day_of_month = monthDay
        self.day_of_week = weekDay
        self.month = month
        self.hour = hour
        self.minute = minute
        self.everyHour = everyHr
        self.everyMin = everyMin
        self.repeat = repeat


    @classmethod
    def create_daily(cls, hour:int, minute:int, everyHr:int, everyMin:int):
        return cls(None, None, None, hour, minute, everyHr, everyMin)
    

    @classmethod
    def create_weekly(cls, weekDay:int, hour:int, minute:int, everyHr:int, everyMin:int):
        return cls(None, weekDay, None, hour, minute, everyHr, everyMin)