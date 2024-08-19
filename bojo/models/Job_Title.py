from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from bojo.models.Scheduled_Run import Base
from bojo.types.experience_types import ExperienceType


class JobTitle(Base):
    __tablename__ = "Job_Titles"
    id = Column(Integer, name="id", primary_key=True, autoincrement=True)
    name = Column(String, name="name", nullable=False, index=True)
    experience_level = Column(Enum(ExperienceType), name="experience_level", nullable=False)
    experience_years = Column(Integer, name="experience_years", nullable=False, default=0)


    def __str__(self):
        return f'JobTitle["id": {str(self.id)}, "name": {self.name}, "experience_level": {self.experience_level.value},"experience_years": {str(self.experience_years)}]'
        

    def __repr__(self):
        return f'JobTitle["id": {str(self.id)}, "name": {self.name}, "experience_level": {self.experience_level.value},"experience_years": {str(self.experience_years)}]'
    
    
    def stringify(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "experience_level": self.experience_level.value,
            "experience_years": str(self.experience_years)
        }