
from sqlalchemy.orm import declarative_base
from bojo.models import Job_Title, Resume, Job_Board, Scheduled_Run, Completed_Run, Application

Base = declarative_base()


def init_db_models(engine):
    Base.metadata.create_all(bind=engine)