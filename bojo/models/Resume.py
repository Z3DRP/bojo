from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from bojo.models.Scheduled_Run import Base


class Resume(Base):
    __tablename__ = "Resumes"
    id = Column(Integer, name="id", primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, name="name", nullable=False, index=True)
    job_title_id = Column(Integer, ForeignKey("Job_Titles.id"), name="job_title_id", nullable=False, index=True)
    file_path = Column(String, name="file_path", nullable=False)

