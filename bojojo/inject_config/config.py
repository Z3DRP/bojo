
from pytest import Session
from bojojo.handlers import db_handler
from bojojo.handlers.db_handler import DbHandler
from bojojo.providers.db_session_provider import session_provider
from bojojo.repositories.Application_Repo import ApplicationRepository
from bojojo.repositories.CompletedRun_Repo import CompletedRunRepository
from bojojo.repositories.JobBoard_Repo import JobBoardRepository
from bojojo.repositories.JobTitle_Repo import JobTitleRepository
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.repositories.ScheduledRun_Repo import ScheduledRunRepository
from bojojo.services.application_service import ApplicationService
from bojojo.services.completedRun_service import CompletedRunService
from bojojo.services.jobBoard_service import JobBoardService
from bojojo.services.jobTitle_service import JobTitleService
from bojojo.services.resume_service import ResumeService
from bojojo.services.scheduledRun_service import ScheduledRunService


def base_config(binder):
    binder.bind(Session, session_provider())
    binder.bind(ResumeRepository, ResumeRepository(Session))
    binder.bind(ResumeService, ResumeService(ResumeRepository))
    binder.bind(ApplicationRepository, ApplicationRepository(Session))
    binder.bind(ApplicationService, ApplicationService(ApplicationRepository))
    binder.bind(CompletedRunRepository, CompletedRunRepository(Session))
    binder.bind(CompletedRunService, CompletedRunService(CompletedRunRepository))
    binder.bind(JobBoardRepository, JobBoardRepository(Session))
    binder.bind(JobBoardService, JobBoardService(JobBoardRepository))
    binder.bind(JobTitleRepository, JobTitleRepository(Session))
    binder.bind(JobTitleService, JobTitleService(JobTitleRepository))
    binder.bind(ScheduledRunRepository, ScheduledRunRepository(Session))
    binder.bind(ScheduledRunService, ScheduledRunService(ScheduledRunRepository))
    binder.bind(db_handler, to=db_handler)


def test_config(binder):
    pass