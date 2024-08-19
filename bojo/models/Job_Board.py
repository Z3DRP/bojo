from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from bojo.models.Scheduled_Run import Base


class JobBoard(Base):
    __tablename__ = "Job_Boards"
    id = Column(Integer, name="id", primary_key=True, autoincrement=True)
    name = Column(String, name="name", nullable=False, index=True)
    url = Column(String, name="url", nullable=False)
    has_easy_apply = Column(Integer, name="has_easy_apply", nullable=False, default=0, index=True)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "has_easy_apply": self.has_easy_apply
        }