from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobBoard(Base):
    __tablename__ = "Job_Boards"
    id = Column(Integer, name="id", primary_key=True)
    name = Column(String, name="name", nullable=False)
    url = Column(String, name="url", nullable=False)
    has_easy_apply = Column(Integer, nullable=False, default=0)