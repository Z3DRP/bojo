from unittest.mock import patch
import pytest
from bojojo import DB_WRITE_ERROR, AddError
from bojojo.repositories import Resume
from bojojo.services.resume_service import ResumeService
from bojojo.repositories.Resume_Repo import ResumeRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.db
@pytest.mark.usefixtures("db_session", "resume_repo", "simulated_db_err", "jobtitle_id", "resume_path", "a_resume")
class TestResumeRepo:

    
    def test_add_resume(self, db_session: Session, resume_repo: ResumeRepository, jobtitle_id: int, resume_path: str):
        resume = Resume(name="dd", valid_jobtitle_id=jobtitle_id, file_path=resume_path)
        new_resume = resume_repo.add(resume)
        db_session.refresh(new_resume)
        assert new_resume.id is not None
        assert new_resume.name == "dd"
        assert new_resume.job_title_id == jobtitle_id
        assert new_resume.file_path == resume_path

    
    def test_add_resume_error(self, resume_repo: ResumeRepository, simulated_db_err: str, mocker):
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        new_resume = Resume(job_title_id=1, file_path="/docs/sm.pdf")
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.add(new_resume)
        assert simulated_db_err in str(exc_info.value)


    def test_get_resume(self, db_session: Session, resume_repo: ResumeRepository, a_resume: Resume):
        resume = a_resume
        db_session.refresh()
        fetched_resume = resume_repo.get(resume.id)
        assert fetched_resume.name == resume.name
        assert fetched_resume.job_title_id == resume.job_title_id
        assert fetched_resume.file_path == resume.file_path