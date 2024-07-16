from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Resume
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.utils import Blogger as blogger
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from typing import List

class ResumeService:
    
    @inject
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
        
    
    def add_resume(self, resume_data:dict) -> Resume:
        try:
            return self.repository.add(**resume_data)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT RESUME ERR] ResumeJobTitleId: {resume_data['job_title_id']}, Path: {resume_data['file_path']}:: {e}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while inserting resume")
        
    
    def update_resume(self, resume_id:int, resume_data:dict) -> Resume:
        try:
            resume = self.get_resume(resume_id)
            if not resume:
                raise GetError(f"Resume with id {resume_id} does not exist")
            return self.repository.update(**resume_data)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise UpdateError(f"DB-ERROR: An error ocurred while updating resume")
    

    def delete_resume(self, id:int):
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE ERR] ResumeId: {id}:: {e}")
            raise DeleteError(f"DB-ERROR: An error ocurred while deleting resume")