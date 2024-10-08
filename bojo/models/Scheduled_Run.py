from sqlalchemy import Boolean, Column, Double, Enum, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from bojo.base_model.base_model import Base
from bojo.types.days import WeekDays
from bojo.types.months import Months
from bojo.types.schedule_types import ScheduleType


class ScheduledRun(Base):
    __tablename__ = "Scheduled_Runs"
    id = Column(Integer, name="id", primary_key=True, autoincrement=True)
    name = Column(String, name="name", nullable=False)
    creation_date = Column(String, name="creation_date", nullable=False)
    job_title_id = Column(Integer, ForeignKey("Job_Titles.id"), name="job_title_id", nullable=False, index=True)
    job_board_id = Column(Integer, ForeignKey("Job_Boards.id"), name="job_board_id", nullable=False, index=True)
    run_day = Column(Integer, name="run_day", nullable=True)
    run_dayOf_week = Column(Enum(WeekDays), name="run_dayOf_week", nullable=True, index=True)
    run_month = Column(Enum(Months), name="run_month", nullable=True)
    run_time = Column(String, name="run_time", nullable=False)
    run_type = Column(Enum(ScheduleType), name="run_type", default=ScheduleType.ONCE, nullable=True)
    recurring = Column(Boolean, name="recurring", default=False)
    easy_apply_only = Column(Boolean, name="easy_apply_only", default=False, nullable=False)
    durration_minutes = Column(Double, name="durration_minutes", nullable=True)
    number_of_submissions = Column(Integer, name="number_of_submissions", nullable=False, default=0)
    every_hour = Column(Integer, name="every_hour", nullable=True)
    every_minute = Column(Integer, name="every_minute", nullable=True)