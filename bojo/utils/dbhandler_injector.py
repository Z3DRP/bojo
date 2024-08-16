

from bojojo import db_path
from bojojo.handlers.db_handler import DbHandler
from bojojo.services.application_service import ApplicationService
from bojojo.services.completedRun_service import CompletedRunService
from bojojo.services.jobBoard_service import JobBoardService
from bojojo.services.jobTitle_service import JobTitleService
from bojojo.services.resume_service import ResumeService
from bojojo.services.scheduledRun_service import ScheduledRunService
from bojojo.utils.service_injector import create_service


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