from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Resume
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.utils import Blogger as blogger
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from typing import List

class ResumeService:
    
    #TODO add blogger.info() for successful actions
    def __init__(self, session: Session, repo: ResumeRepository):
        self.repository = repo


    def get_resume(self, resume_id: int) -> Resume:
        try:
            return self.repository.get(resume_id)
        except SQLAlchemyError as e:
            blogger.error(f"[ERR; ResumeId: {resume_id}] The following error ocurred: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        

    def get_all_resumes(self) -> List[Resume]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[ERR] The folling error ocurred while reading: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def add_resume(self, job_title_id: int, file_path: str) -> Resume:
        try:
            resume = Resume(job_title_id=job_title_id, file_path=file_path)
            blogger.info(f"Resume added: [id: {resume.id}, jobTitleId: {resume.job_title_id}], path: {resume.file_path}")
            return self.repository.add(resume)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT ERR: ResumeJobTitleId: {job_title_id}; Path: {file_path}] The following error ocurred while inserting resume {e}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while inserting resume")
        
    
    def update_resume(self, resume_id: int, job_title_id: int, file_path: str) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            resume.job_title_id = job_title_id
            resume.file_path = file_path
            return self.repository.update(resume)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE ERR: ResumeId: {resume_id}; JobTitleId: {job_title_id}; Path: {file_path}] The following error ocurred while updating resume {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume")
        
        
    def update_job_title_id(self, resume_id: int, job_title_id: int) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update_job_title(resume_id=resume_id, job_title_id=job_title_id)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE ERR: ResumeId: {resume_id}; JobTitleId: {job_title_id}] The following error ocurred while updating resume job title id {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume job title id")
        

    def update_file_path(self, resume_id: int, path: str) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update_path(resume_id=resume_id, file_path=path)
        except SQLAlchemyError as e:
            blogger(f"[UPDATE ERR: ResumeId: {resume_id}; FilePath: {path}] The following error ocurred while updating resume file path {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume file path")