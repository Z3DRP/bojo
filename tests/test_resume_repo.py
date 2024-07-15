from unittest.mock import patch
import pytest
from sqlalchemy import text
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
        resume = {'name': 'dd', 'job_title_id': jobtitle_id, 'file_path': resume_path}
        new_resume = resume_repo.add(resume)
        db_session.refresh(new_resume)
        assert new_resume.id is not None
        assert new_resume.name == "dd"
        assert new_resume.job_title_id == jobtitle_id
        assert new_resume.file_path == resume_path

    
    def test_add_resume_error(self, resume_repo: ResumeRepository, simulated_db_err: str, mocker):
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        new_resume = {'id': 1, 'name': 'dd', 'job_title_id': 1, 'file_path': '/docs/sm.pdf'}
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.add(new_resume)
        assert simulated_db_err in str(exc_info.value)


    def test_get_resume(self, db_session: Session, resume_repo: ResumeRepository, a_resume: Resume):
        resume = a_resume
        db_session.refresh(resume)
        fetched_resume = resume_repo.get(resume.id)
        assert fetched_resume.name == resume.name
        assert fetched_resume.job_title_id == resume.job_title_id
        assert fetched_resume.file_path == resume.file_path

    
    def test_get_resume_error(self, db_session: Session, resume_repo: ResumeRepository, jobtitle_id: str, simulated_db_err: str, mocker):
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        resume = Resume(id=1, name="dd", job_title_id=jobtitle_id, file_path="docs/rsm.pdf")
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.get(resume.id)
        assert simulated_db_err in str(exc_info.value)

    
    def test_get_all_resume(self, db_session: Session, resume_repo: ResumeRepository, a_resume: Resume, b_resume):
        resume1 = a_resume
        resume2 = b_resume
        db_session.refresh(resume1)
        db_session.refresh(resume2)
        resumes = resume_repo.getAll()
        assert len(resumes) == 2


    def test_get_all_resume_error(self, simulated_db_err: str, resume_repo: ResumeRepository, a_resume: Resume, mocker):
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        resume = Resume(id=1, name="tst", job_title_id=1, file_path="docs/rsm.pdf")
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.getAll()
        assert simulated_db_err in str(exc_info.value)

    
    def test_update_resume(self, db_session: Session, a_resume: Resume, resume_repo: ResumeRepository):
        resume = {'id': a_resume.id, 'name': a_resume.name, 'file_path': a_resume.file_path}
        updated_resume = resume_repo.update(resume)
        db_session.refresh(resume)
        assert updated_resume.rowcount == 2
        assert updated_resume.name == 'tster'
        assert updated_resume.file_path == 'new/path'

    
    def test_update_resume_error(self, resume_repo: ResumeRepository, simulated_db_err: str, a_resume: Resume, mocker):
        resume = {'id': a_resume.id, 'name': a_resume.name, 'file_path': a_resume.file_path}
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.update(resume)
        assert simulated_db_err in str(exc_info.value)

    
    def test_delete_resume(self, db_session: Session, resume_repo: ResumeRepository, a_resume: Resume):
        resume = a_resume
        del_resume = resume_repo.delete(resume.id)
        assert del_resume.rowcount == 1
        dresume = db_session.execute(
            text("SELECT * FROM Resumes WHERE id = :rid"),
            {'rid': resume.id}
        )
        assert dresume is None


    def test_delete_resume_error(self, db_session: Session, resume_repo: ResumeRepository, a_resume: Resume, simulated_db_err: str, mocker):
        mocker.patch.object(Session, 'execute', side_effect=SQLAlchemyError(simulated_db_err))
        resume = a_resume
        with pytest.raises(SQLAlchemyError) as exc_info:
            resume_repo.delete(resume.id)
        assert simulated_db_err in str(exc_info.value)

