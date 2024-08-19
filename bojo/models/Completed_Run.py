from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from bojo.models.Scheduled_Run import Base


class CompletedRun(Base):
    __tablename__ = "Completed_Runs"
    id = Column(Integer, name="id", primary_key=True, nullable=False, autoincrement=True)
    execution_date = Column(String, name="execution_date", nullable=False, index=True)
    start = Column(String, name="start", nullable=False)
    finish = Column(String, name="finish", nullable=False)
    applications_submitted = Column(Integer, name="applications_submitted", nullable=False, index=True)
    failed_submissions = Column(Boolean, name="failed_submissions", nullable=False, default=False, index=True)
    run_id = Column(Integer, ForeignKey("Scheduled_Runs.id"), name="run_id", nullable=False, index=True)