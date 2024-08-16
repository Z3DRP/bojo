from injector import Module, singleton, provider
from sqlalchemy.orm import Session
from generators import DbGenerator
from repositories import ApplicationRepository, CompletedRunRepository, JobBoardRepository, JobTitleRepository, ResumeRepository, ScheduledRunRepository
from services import ApplicationService, CompletedRunService, JobBoardService, JobTitleService, ResumeService, ScheduledRunService


class DatabaseSessionProvider:

    def __init__(self, db_path:str):
        self.db = DbGenerator(db_path=db_path)


    @singleton
    @provider
    def provide(self) -> Session:
        return next(self.db.generate_db())
    

class AppModule(Module):
    def configure(self, binder):
        binder.bind(Session, to=DatabaseSessionProvider, scope=singleton)
        binder.bind(ResumeRepository, to=ResumeRepository, scope=singleton)
        binder.bind(ApplicationRepository, to=ApplicationRepository, scope=singleton)
        binder.bind(CompletedRunRepository, to=CompletedRunRepository, scope=singleton)
        binder.bind(JobBoardRepository, to=JobBoardRepository)
        binder.bind(JobTitleRepository, to=JobTitleRepository, scope=singleton)
        binder.bind(ScheduledRunRepository, to=ScheduledRunRepository, scope=singleton)
        binder.bind(ApplicationService, to=ApplicationService, scope=singleton)
        binder.bind(CompletedRunService, to=CompletedRunService, scope=singleton)
        binder.bind(JobTitleService, to=JobTitleService, scope=singleton)
        binder.bind(JobBoardService, to=JobBoardService, scope=singleton)
        binder.bind(CompletedRunService, to=CompletedRunService, scope=singleton)
        binder.bind(ResumeService, to=ResumeService, scope=singleton)
        binder.bind(ScheduledRunService, to=ScheduledRunService, scope=singleton)