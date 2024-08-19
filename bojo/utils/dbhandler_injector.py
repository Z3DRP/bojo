

from bojo import db_path
from bojo.handlers.db_handler import DbHandler
from bojo.services.application_service import ApplicationService
from bojo.services.completedRun_service import CompletedRunService
from bojo.services.jobBoard_service import JobBoardService
from bojo.services.jobTitle_service import JobTitleService
from bojo.services.resume_service import ResumeService
from bojo.services.scheduledRun_service import ScheduledRunService
from bojo.utils.service_injector import create_service


def inject_handler():
    return DbHandler(
        db_path(),
        appServ=create_service(ApplicationService),
        compServ=create_service(CompletedRunService),
        jobBoardServ=create_service(JobBoardService),
        jobTitleServ=create_service(JobTitleService),
        resumeServ=create_service(ResumeService),
        schedServ=create_service(ScheduledRunService)
    )