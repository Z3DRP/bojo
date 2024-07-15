from pathlib import Path
from bojojo.adapters import CurrentItem, DbResponse
from bojojo.services import ApplicationService, CompletedRunService, JobBoardService, JobTitleService, ResumeService, ScheduledRunService

class DbHandler:

    def __init__(self, db_path: Path, appService: ApplicationService, completedRunService: CompletedRunService, jobBoardService: JobBoardService,
                 jobTitleService: JobTitleService, resumeService: ResumeService, scheduledRunService: ScheduledRunService) -> None:
        self.__db_path = db_path
        self.appService = appService
        self.completedRunService = completedRunService
        self.jobBoardService = jobBoardService
        self.jobTitleService = jobTitleService
        self.resumeService = resumeService
        self.scheduledRunService = scheduledRunService

    def 