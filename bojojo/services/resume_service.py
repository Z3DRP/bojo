from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Resume
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.utils import Blogger as blogger
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from typing import List

class ResumeService:
    

    def __init__(self, repo: ResumeRepository):
        self.repository = repo


    def get_resume(self, resume_id: int) -> Resume:
        try:
            return self.repository.get(resume_id)
        except SQLAlchemyError as e:
            blogger.error(f"[READ ERR] ResumeId: {resume_id}:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        

    def get_all_resumes(self) -> List[Resume]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[READ ERR]:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def add_resume(self, name: str, job_title_id: int, file_path: str) -> Resume:
        try:
            resume = Resume(name="dd", job_title_id=job_title_id, file_path=file_path)
            return self.repository.add(resume)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT RESUME ERR] ResumeJobTitleId: {job_title_id}, Path: {file_path}:: {e}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while inserting resume")
        
    
    def update_resume(self, resume_id: int, name: str, job_title_id: int, file_path: str) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            resume.name = name
            resume.job_title_id = job_title_id
            resume.file_path = file_path
            return self.repository.update(resume)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume")
        
        
    def update_job_title_id(self, resume_id: int, job_title_id: int) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update_job_title(resume_id=resume_id, job_title_id=job_title_id)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume job title id")
        

    def update_file_path(self, resume_id: int, path: str) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update_path(resume_id=resume_id, file_path=path)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume file path")
        
    
    def update_name(self, resume_id: int, name: str):
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update_name(resume_id=resume_id, name=name)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise UpdateError(f"DB-Error: An error ocurred while updating resume name")
        