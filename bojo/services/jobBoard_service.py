from typing import List
import inject
from pytest import Session
from bojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, DeleteError, GetError, UpdateError
from bojo.base_service import Service
from bojo.models.Job_Board import JobBoard
from bojo.repositories.JobBoard_Repo import JobBoardRepository
from sqlalchemy.exc import SQLAlchemyError

from bojo.utils.bologger import Blogger
from bojo.utils.repo_injector import create_repo

class JobBoardService(Service):
    

    # repository = inject.attr(JobBoardRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        self.repository = create_repo(repo_type=JobBoardRepository)

    
    def get_job_board(self, id:int) -> JobBoard:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-BOARD ERR] JobId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_jobBoard_by_name(self, jname:str) -> JobBoard:
        try:
            return self.repository.getByName(jname)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-BOARD ERR] JobBoardName: {jname}:: {e}")
            raise GetError(DB_WRITE_ERROR, e._message)
        
    
    def get_all_jobBoards(self) -> List[JobBoard]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ JOB-BOARD ERR] :: {e}")
            raise AddError(DB_WRITE_ERROR, e._message)
        
    
    def add_job_board(self, board_data:dict) -> JobBoard:
        try:
            return self.repository.add(board_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT JOB-BOARD ERR] JobBoardName: {board_data}")
            raise AddError(DB_WRITE_ERROR, e._message)
    

    def update_job_board(self, id:int, board_data:dict) -> JobBoard:
        try:
            jboard = self.get_job_board(id)
            if not jboard:
                raise GetError(f"Job Board with id: {id} does not exist")
            return self.repository.update(id, **board_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE JOB-BOARD ERR] JobBoardId: {id}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def update_jobboard_byName(self, name:str, board:dict) -> JobBoard:
        try:
            jboard = self.get_jobBoard_by_name(name)
            if not jboard:
                raise GetError(f"Job Board with name: {name} does not exist")
            return self.repository.update_by_name(name, board)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE JOB-BOARD ERR] JobBoardName: {name}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def delete_job_board(self, id:int) -> int:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-BOARD ERR] JobBoardId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_all_jobBoards(self) -> int:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-BOARD ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_jobBoard_byName(self, name:str) -> int:
        try:
            return self.repository.delete_by_name(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-BOARD ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        