
from sqlalchemy import Column, ForeignKey, Integer, String

from bojo.models.Scheduled_Run import Base


class FailedSubmission(Base):
    __tablename__ = "failedSubmissions"
    id = Column(Integer, primarykey=True, nullable=False, autoincrement=True)
    completedRunId = Column(Integer, ForeignKey("CompletedRuns.id"), name="completedRunId", nullable=False, index=True)
    applicationUrl = Column(String, nullable=False, name="applicationUrl", nullable=False, index=True)
    missingFields = Column(String, nullable=False, name="missingFields", nullable=False)