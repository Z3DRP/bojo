from unittest.mock import patch
import pytest
from bojojo import DB_WRITE_ERROR, AddError, GetError, UpdateError
from bojojo.repositories import Resume
from bojojo.services.resume_service import ResumeService
from bojojo.repositories.Resume_Repo import ResumeRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.service
@pytest.mark.usefixtures("sqlite_db", "session", "simulated_db_err", "valid_jobtitle_id", "mock_resume_service", "mock_resume_repo", "resume_path")
class TestResumeService:

    
    def test_add_resume(self, mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str):
        mock_resume_repo.add.return_value = Resume(id=1, name="dd", job_title=1, file_path=resume_path)
        new_resume = mock_resume_service.add_resume({'name': 'dd', 'job_title_id': 1, 'file_path': resume_path})
        assert new_resume.name == 'dd'
        assert new_resume.job_title_id == 1
        assert new_resume.file_path == resume_path


    def test_add_resume_error(self, mock_resume_service: ResumeService, mock_resume_repo: ResumeRepository, simulated_db_err: str):
        mock_resume_repo.add.side_effect = SQLAlchemyError(simulated_db_err)
        with patch.object('bojojo.services.resume_service.blogger.error') as mock_logger:
            with pytest.raises(AddError) as exc_info:
                mock_resume_service.add_resume({'name': 'dd', 'job_title_id': 1, 'file_path': "/some/arbitrary/path"})
            assert exc_info.value.code == DB_WRITE_ERROR
            assert "DB-ERROR" in str(exc_info.value)
            mock_logger.assert_called_with(f"[INSERT RESUME ERR] ResumeJobTitleId: 1, Path: /some/arbitrary/path:: Simulated DB error")

    
    def test_get_resume(self, mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str):
        mock_resume_repo.get.return_value = Resume(id=1, name="dd", job_title_id=1, file_path=resume_path)
        resume = mock_resume_service.get_resume(1)
        assert resume.id == 1
        assert resume.name == 'dd'
        assert resume.job_title_id == 1
        assert resume.file_path == resume_path


    def test_get_all_resumes(self, mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str):
        mock_resume_repo.get.return_value = [Resume(id=1, name="dd", job_title_id=1, file_path=resume_path), Resume(id=2, name="dt", job_title_id=2, file_path=resume_path)]
        resumes = mock_resume_service.get_all_resumes()
        assert len(resumes) == 2

    
    def test_update_resume(mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str):
        mock_resume_repo.get.return_value = Resume(id=1, name="dd", job_title_id=1, file_path=resume_path)
        mock_resume_repo.update.return_value = Resume(id=1, name="dd", job_title_id=2, file_path=f"new/{resume_path}")
        updated_resume = mock_resume_service.update_resume({'id': 1, 'name': 'dd', 'job_title_id': 2, 'file_path': f"/new{resume_path}"})
        assert updated_resume.name == 'dd'
        assert updated_resume.job_title_id == 2
        assert updated_resume.file_path == f"new/{resume_path}"


    def test_update_resume_notfound(self, mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str):
        mock_resume_repo.get.return_value = None
        with pytest.raises(GetError) as exc_info:
            mock_resume_service.update_resume({'id': 1, 'name': 'dd', 'job_title_id': 2, 'file_path': f"new/{resume_path}"})
        assert "1 does not exist" in str(exc_info.value)

    
    def test_update_resume_error(self, mock_resume_repo: ResumeRepository, mock_resume_service: ResumeService, resume_path: str, simulated_db_err: str):
        mock_resume_repo.get.return_value = Resume(id=1, name="dd", job_title_id=1, file_path=resume_path)
        mock_resume_repo.update.side_effect = SQLAlchemyError(simulated_db_err)
        with patch.object('bojojo.services.resume_service.blogger.error') as mock_logger:
            with pytest.raises(UpdateError) as exc_info:
                mock_resume_service.update_resume({'id': 1, 'name': 'dd', 'job_title_id': 2, 'file_path': f"new/{resume_path}"})
            assert "DB-ERROR" in str(exc_info.value)
            mock_logger.assert_called_with('[UPDATE RESUME ERR] ResumeId: 1:: Simulated DB error')

