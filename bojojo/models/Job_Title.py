from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from bojojo.types.experience_types import ExperienceType

Base = declarative_base()

class JobTitle(Base):
    __tablename__ = "Job_Titles"
    id = Column(Integer, name="id", primary_key=True, autoincrement=True)
    name = Column(String, name="name", nullable=False, index=True)
    experience_level = Column(Enum(ExperienceType), name="experience_level", nullable=False)
    experience_years = Column(Integer, name="experience_years", nullable=False, default=0)