
from pytest import Session
from bojo import db_path
from bojo.handlers.db_handler import DbHandler
from bojo.providers.db_session_provider import session_provider
from bojo.repositories.Application_Repo import ApplicationRepository
from bojo.repositories.CompletedRun_Repo import CompletedRunRepository
from bojo.repositories.JobBoard_Repo import JobBoardRepository
from bojo.repositories.JobTitle_Repo import JobTitleRepository
from bojo.repositories.Resume_Repo import ResumeRepository
from bojo.repositories.ScheduledRun_Repo import ScheduledRunRepository
from bojo.services.application_service import ApplicationService
from bojo.services.completedRun_service import CompletedRunService
from bojo.services.jobBoard_service import JobBoardService
from bojo.services.jobTitle_service import JobTitleService
from bojo.services.resume_service import ResumeService
from bojo.services.scheduledRun_service import ScheduledRunService
from bojo.utils.config_reader import get_db_path
from bojo.utils.bologger import Blogger
from bojo.utils.db_session import DbSession


def base_config(binder):
    binder.bind_to_provider(Session, session_provider)
    # binder.bind(DbSession, DbSession())
    # binder.bind(ResumeRepository, ResumeRepository())
    # binder.bind(ApplicationRepository, ApplicationRepository())
    # binder.bind(CompletedRunRepository, CompletedRunRepository())
    # binder.bind(JobBoardRepository, JobBoardRepository())
    # binder.bind(JobTitleRepository, JobTitleRepository())
    # binder.bind(ScheduledRunRepository, ScheduledRunRepository())
    # binder.bind(ResumeService, ResumeService())
    # binder.bind(ApplicationService, ApplicationService())
    # binder.bind(CompletedRunService, CompletedRunService())
    # binder.bind(JobBoardService, JobBoardService())
    # binder.bind(JobTitleService, JobTitleService())
    # binder.bind(ScheduledRunService, ScheduledRunService())
    # binder.bind(DbHandler, DbHandler(db_path()))
    binder.bind(Blogger, Blogger())


def test_config(binder):
    pass