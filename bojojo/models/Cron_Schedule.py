
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
        self.previous = None
        self.next = None
        self.isValid = None
        self.isEnabled = None

    
    def setPrevious(self, prev):
        self.previous = prev
    
    def getPrevious(self):
        return self.previous
    
    def setNext(self, nextRun):
        self.next = nextRun

    def getNext(self):
        return self.next
    
    def setIsValid(self, valid):
        self.isValid = valid
    
    def getIsValid(self):
        return self.isValid
    
    def setIsEnabled(self, enabled):
        self.isEnabled = enabled
    
    def getIsEnabled(self):
        return self.isEnabled
