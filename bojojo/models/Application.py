from sqlalchemy import Column, Integer, String, Double, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Application(Base):
    __tablename__ = "Applications"
    id = Column(Integer, name="id", primary_key=True)
    company = Column(String, name="company", nullable=False)
    job_title = Column(String, name="job_title", nullable=False)
    location = Column(String, name="location", nullable=False)
    pay = Column(Double, name="pay", nullable=True)
    apply_date = Column(String, nullable=False)
    submitted_successfully = Column(Integer, name="submitted_successfully", nullable=False, default=0)
    run_id = Column(Integer, ForeignKey("Completed_Runs.id"), name="run_id")
