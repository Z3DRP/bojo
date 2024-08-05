import inject
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Resume
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.utils.bologger import Blogger
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from typing import List

class ResumeService:
    
    
    repository = inject.attr(ResumeRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        pass


    def get_resume(self, resume_id: int) -> Resume:
        try:
            return self.repository.get(resume_id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ RESUME ERR] ResumeId: {resume_id}:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_resume_byName(self, name:str) -> Resume:
        try:
            return self.repository.getByName(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ RESUME ERR] ResumeName: {name}:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        

    def get_all_resumes(self) -> List[Resume]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ ERR]:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def add_resume(self, resume_data:dict) -> Resume:
        try:
            return self.repository.add(**resume_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT RESUME ERR] ResumeJobTitleId: {resume_data['job_title_id']}, Path: {resume_data['file_path']}:: {e}")
            raise AddError(DB_WRITE_ERROR, e._message)
        
    
    def update_resume(self, resume_name:str, resume_data:dict) -> Resume:
        try:
            resume = self.get_resume(resume_name)
            if not resume:
                raise GetError(f"Resume with id {resume_name} does not exist")
            return self.repository.update(**resume_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE RESUME ERR] ResumeId: {resume_name}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
    

    def delete_resume(self, name:str) -> Resume:
        try:
            return self.repository.delete(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE RESUME ERR] ResumeId: {name}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_all_resumes(self) -> Resume:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE RESUME ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)