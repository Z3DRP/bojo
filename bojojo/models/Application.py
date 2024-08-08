from sqlalchemy import Boolean, Column, Integer, String, Double, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from bojojo.base_model import Base

class Application(Base):
    __tablename__ = "Applications"
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    company = Column(String, name="company", nullable=False, index=True)
    job_title_id = Column(Integer, ForeignKey("Job_Titles.id"), name="job_title_id", nullable=False, index=True)
    job_board_id = Column(Integer, ForeignKey("Job_Boards.id"), name="job_board_id", nullable=False, index=True)
    location = Column(String, name="location", nullable=False)
    pay = Column(Double, name="pay", nullable=True)
    apply_date = Column(String, nullable=False)
    submitted_successfully = Column(Boolean, name="submitted_successfully", nullable=False, default=False, index=True)
    run_id = Column(Integer, ForeignKey("Completed_Runs.id"), name="run_id", nullable=False)
