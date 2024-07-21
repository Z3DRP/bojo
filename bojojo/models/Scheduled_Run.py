from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScheduledRun(Base):
    __tablename__ = "Scheduled_Runs"
    id = Column(Integer, name="id", primary_key=True)
    name = Column(String, name="name")
    creation_date = Column(String, name="creation_date", nullable=False)
    job_title_id = Column(Integer, ForeignKey("Job_Titles.id"), name="job_title_id", nullable=False)
    job_board_id = Column(Integer, ForeignKey("Job_Boards.id"), name="job_board_id", nullable=False)
    run_date = Column(String, name="run_date")
    run_dayOf_week = Column(String, name="run_dayOf_week")
    run_time = Column(String, name="run_time", nullable=False)
    run_type = Column(String, name="run_type", nullable=False, default="once")
    recurring = Column(Integer, name="recurring", nullable=False, default=0)
    easy_apply_only = Column(Integer, name="easy_apply_only", nullable=False, default=0)