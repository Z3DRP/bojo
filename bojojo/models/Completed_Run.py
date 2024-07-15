from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CompletedRun(Base):
    __tablename__ = "Completed_Runs"
    id = Column(Integer, name="id", primary_key=True)
    execution_date = Column(String, name="execution_date", nullable=False)
    start = Column(String, name="start", nullable=False)
    finish = Column(String, name="finish", nullable=False)
    applications_submitted = Column(Integer, name="applications_submitted", nullable=False)
    failed_submissions = Column(Integer, name="failed_submissions", nullable=False, default=0)
    run_id = Column(Integer, ForeignKey("Scheduled_Runs.id"), name="run_id")