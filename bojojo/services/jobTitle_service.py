from typing import List
import inject
from sqlalchemy.exc import SQLAlchemyError
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from bojojo.base_service import Service
from bojojo.models.Job_Title import JobTitle
from bojojo.repositories.JobTitle_Repo import JobTitleRepository
from bojojo.utils.bologger import Blogger
from bojojo.utils.repo_injector import create_repo


class JobTitleService(Service):

    
    # repository = inject.attr(JobTitleRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        self.repository = create_repo(repo_type=JobTitleRepository)
        #pass
    

    def get_job_title(self, id:int) -> JobTitle:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-TITLE ERR] JobTitleId: {id}:: {e}")
            raise GetError(DB_WRITE_ERROR, e._message)

    
    def get_job_title_by_name(self, title:str) -> JobTitle:
        try:
            return self.repository.getByName(title)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-TITLE ERR] JobTitleName: {title}:: {e}")
            raise GetError(DB_WRITE_ERROR, e._message)


    def get_all_jobTitles(self) -> List[JobTitle]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-TITLE ERR]:: {e}")
            raise GetError(DB_WRITE_ERROR, e._message)
        
    
    def add_job_title(self, job_data:dict) -> JobTitle:
        try:
            return self.repository.add(job_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT JOB-TITLE ERR] JobTitleId: {job_data}:: {e}")
            raise AddError(DB_WRITE_ERROR, e._message)
    

    def update_job_title(self, id:int, job_data:dict) -> JobTitle:
        try:
            jobTitle = self.get_job_title(id)
            if not jobTitle:
                raise GetError(f"Job Title with id: {id} does not exist")
            return self.repository.update(id, job_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE JOB-TITLE ERR] JobTitleId: {id}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def update_jobTitle_byName(self, name:str, job_data:dict) -> JobTitle:
        try:
            jobTitle = self.get_job_title_by_name(name)
            if not jobTitle:
                raise GetError(f"Job Title with name: {name} does not exist")
            return self.repository.update_by_name(name, job_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE JOB-TITLE ERR] JobTitleName: {name}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def delete_job_title(self, id:int) -> int:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-TITLE ERR] JobTitleId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_jobTitle_byName(self, name:str) -> int:
        try:
            return self.repository.delete_by_name(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-TITLE ERR] JobTitleName: {name}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_all_jobTitles(self) -> int:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-TITLE ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        