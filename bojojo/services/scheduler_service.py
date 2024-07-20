from crontab import CronTab

class SchedulerService:
    
    def __init__(self):
        self.cron = CronTab(user=True)
        self.bojoRunnerPath = "/path/to/update/for/autoApply"
        self.command = f"python3 {self.bojoRunnerPath}"
        self.schedule = None
        self.job = self.cron.new(command=self.command)


    def scheduleJob(self, schedule: str) -> None:
        self.setall(schedule)
        self.cron.write()

    @classmethod
    def getScheduler(cls):
        return cls()
    

    def removeAllScheduledJobs(self) -> None:
        self.cron.remove_all()
        self.cron.write()

    
    def removeScheduledJob(self, schedule:str) -> None: 
        jobCount = 0
        for job in self.cron:
            if job.slices == schedule:
                self.cron.remove(job)
                jobCount += 1
        if jobCount > 0:
            self.cron.write()
        