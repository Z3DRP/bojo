
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
from bojojo.utils.config_reader import get_db_path


def base_config(binder):
    binder.bind(Session, session_provider())
    binder.bind(ResumeRepository, ResumeRepository())
    binder.bind(ApplicationRepository, ApplicationRepository())
    binder.bind(CompletedRunRepository, CompletedRunRepository())
    binder.bind(JobBoardRepository, JobBoardRepository())
    binder.bind(JobTitleRepository, JobTitleRepository())
    binder.bind(ScheduledRunRepository, ScheduledRunRepository())
    binder.bind(ResumeService, ResumeService)
    binder.bind(ApplicationService, ApplicationService)
    binder.bind(CompletedRunService, CompletedRunService)
    binder.bind(JobBoardService, JobBoardService)
    binder.bind(JobTitleService, JobTitleService)
    binder.bind(ScheduledRunService, ScheduledRunService)
    binder.bind(db_handler, db_handler(get_db_path()))


def test_config(binder):
    pass