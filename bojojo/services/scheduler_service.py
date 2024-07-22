from crontab import CronTab

from bojojo.models.Cron_Schedule import CronSchedule

class SchedulerService:
    
    def __init__(self, cronSchedule, *args):
        # might have to update to user created in docker container
        self.cron = CronTab(user='root')
        self.bojoRunnerPath = "/path/to/update/for/autoApply"
        # wil need need add arguements to be passed to path for applier script
        self.scriptArguements = None
        for arg in args:
            self.scriptArguements += f' "{arg}"'
        self.command = f'python3 {self.bojoRunnerPath} {self.scriptArguements} "{cronSchedule.durration}" "{cronSchedule.numberOfSubmissions}"'
        self.cronSchedule = cronSchedule
        self.job = self.cron.new(command=self.command, comment=self.cronSchedule.name)
        self.schedule = None
        self.configureJobSchedule()
    

    def configureJobSchedule(self):
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
        self.writeJob()


    def writeJob(self) -> None:
        self.cron.write()
    

    #TODO change method to be static so it can just iter crontabs and remove
    def removeAllScheduledJobs(self) -> None:
        self.cron.remove_all()
        self.cron.write()


    #TODO change method to be static so it can just iter crontabs and remove
    def removeScheduledJob(self, schedule:str) -> None: 
        jobCount = 0
        for job in self.cron:
            if job.slices == schedule:
                self.cron.remove(job)
                jobCount += 1
        if jobCount > 0:
            self.cron.write()

    
    @classmethod
    def getScheduler(cls, sched:CronSchedule, argList):
        return cls(sched, argList)
            
        