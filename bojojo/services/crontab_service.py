import datetime
from crontab import CronTab

from bojojo import CRON_NOT_FOUND, SUCCESS, NoCronJobFound
from bojojo.models.Cron_Schedule import CronSchedule

class CronTabService:
    
    def __init__(self):
        self.initailize_cron()
        self.bojoRunnerPath = "/path/to/update/for/autoApply"
        # wil need need add arguements to be passed to path for applier script
        self.scriptArguements = None
        self.command = None
        self.cronSchedule = None
        self.job = None
        self.schedule = None

    
    def initailize_cron(self):
        # might have to update to user created in docker container
        self.cron = CronTab(user='root')

    
    def configureJob(self, cronSchedule, *args) -> None:
        for arg in args:
            self.scriptArguements += f' "{arg}"'
        self.command = f'python3 {self.bojoRunnerPath} {self.scriptArguements} "{cronSchedule.durration}" "{cronSchedule.numberOfSubmissions}"'
        self.cronSchedule = cronSchedule
        self.job = self.cron.new(command=self.command, comment=self.cronSchedule.name)
        self.schedule = None
        self.configureJobSchedule() 
    

    def configureSchedule(self):
        if self.cronSchedule.dayOfWeek:
            self.job.dow.on(self.dayOfWeek)
        if self.cronSchedule.month:
            self.job.month.during(self.month)
        if self.cronSchedule.dayOfMonth:
            self.job.day.on(self.dayOfMonth)
        if self.cronSchedule.hour:
            self.job.hour(self.hour)
        if self.cronSchedule.minute:
            self.job.minute(self.minute)
        if self.cronSchedule.everyHour:
            self.job.hour.every(self.everyHour)
        if self.cronSchedule.everyMintute:
            self.job.minute.every(self.everyMinute)
        if not self.cronSchedule.hour and not self.cronSchedule.minute and self.cronSchedule.daily:
            self.job.setall("@daily")
        if self.cronSchedule.hour and self.cronSchedule.minute and self.cronSchedule.daily:
            self.job.setall(f"{self.minute} {self.hour} * * *")
        if not self.cronSchedule.hour and not self.cronSchedule.minute and self.cronSchedule.weekly:
            self.job.setall("@weekly")
        if self.cronSchedule.hour and self.cronSchedule.minute and not self.cronSchedule.dayOfWeek and self.cronSchedule.weekly:
            self.job.setall(f"{self.minute} {self.hour} * * 1")
        if self.cronSchedule.hour and self.cronSchedule.minute and self.cronSchedule.dayOfWeek and self.cronSchedule.weekly:
            self.job.setall(f"{self.minute} {self.hour} * * {self.dayOfWeek}")
        try:
            self.writeJob()
        except RuntimeError as e:
            raise e


    def writeJob(self) -> None:
        self.cron.write()
    

    @classmethod
    def removeAllScheduledJobs(cls) -> None:
        service = cls()
        try:
            service.cron.remove_all()
            service.cron.write()
            return SUCCESS
        except Exception as e:
            return e


    @classmethod
    #TODO change method to be static so it can just iter crontabs and remove
    def removeScheduledJob(cls, scheduleName:str) -> None: 
        service = cls()
        jobCount = 0
        jobIter = service.cron.find_comment(scheduleName)
        if not jobIter:
            return CRON_NOT_FOUND
        for job in jobIter:
            service.cron.remove(job)
            jobCount += 1
        if jobCount > 0:
            service.cron.write()
        return SUCCESS

    
    @classmethod
    def getScheduler(cls, sched:CronSchedule, argList):
        return cls().configureJob(sched, argList)
    
    
    @classmethod
    def getNext(cls, sched:CronSchedule) -> datetime:
        service = cls()
        cronjob = service.cron.find_comment(sched.name)
        nextExc = None
        for job in cronjob:
            schedule = job.schedule(date_from=datetime.now())
            nextExc = schedule.get_next()
        return nextExc
    

    @classmethod
    def getPrevious(cls, sched:CronSchedule) -> datetime:
        service = cls()
        cronjob = service.cron.find_comment(sched.name)
        prevExc = None
        for job in cronjob:
            schedule = job.schedule(date_from=datetime.now())
            prevExc = schedule.get_previous()
        return prevExc


    @classmethod
    def isValid(cls, sched:CronSchedule) -> bool:
        service = cls()
        cronjob = service.cron.find_comment(sched.name)
        isvalid = False
        for job in cronjob:
            isvalid = job.is_valid()
        return isvalid

    @classmethod
    def isEnabled(cls, sched:CronSchedule) -> bool:
        service = cls()
        cronjob = service.cron.find_comment(sched.name)
        isenabled = False
        for job in cronjob:
            isenabled = job.is_enabled()
        return isenabled