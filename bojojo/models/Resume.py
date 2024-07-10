from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Resume(Base):
    __tablename__ = "Resumes"
    id = Column(Integer, name="id", primary_key=True)
    job_title_id = Column(Integer, ForeignKey("Job_Titles.id"), name="job_title_id")
    file_path = Column(String, name="file_path", nullable=False)

