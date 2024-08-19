import inject
from sqlalchemy.exc import SQLAlchemyError
from bojo.base_service import Service
from bojo.models import Resume
from bojo.repositories.Resume_Repo import ResumeRepository
from bojo.utils.bologger import Blogger
from bojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from typing import List

from bojo.utils.repo_injector import create_repo

class ResumeService(Service):
    
    
    # repository = inject.attr(ResumeRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        self.repository = create_repo(repo_type=ResumeRepository)


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
            return self.repository.add(resume_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT RESUME ERR] ResumeJobTitleId: {resume_data['job_title_id']}, Path: {resume_data['file_path']}:: {e}")
            raise AddError(DB_WRITE_ERROR, e._message)
        
    
    def update_resume(self, id:int, resume_data:dict) -> Resume:
        try:
            resume = self.repository.get(id)
            if not resume:
                raise GetError(f"Resume with id {id} does not exist")
            return self.repository.update(id, resume_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE RESUME ERR] ResumeId: {id}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def update_resume_byName(self, name:str, resume_data:dict) -> Resume:
        try:
            resume = self.repository.getByName(id)
            if not resume:
                raise GetError(f"Resume with name: {name} does not exist")
            return self.repository.update_by_name(name, resume_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE RESUME ERR] ResumeName: {name}:: {e}")
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