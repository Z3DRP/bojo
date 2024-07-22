from typing import List

from injector import inject
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, AddError, DeleteError, GetError, UpdateError
from bojojo.models.Job_Board import JobBoard
from bojojo.repositories.JobBoard_Repo import JobBoardRepository
from sqlalchemy.exc import SQLAlchemyError
from bojojo.utils.bologger import blogger as blogger
class JobBoardService:
    
    @inject
    def __init__(self, repo: JobBoardRepository):
        self.repository = repo

    
    def get_job_board(self, id:int) -> JobBoard:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            blogger.error(f"[READ JOB-BOARD ERR] JobId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, f"DB-ERROR: An error occurred while reading")
        
    
    def get_jobBoard_by_name(self, jname:str) -> JobBoard:
        try:
            return self.repository.getByName(jname)
        except SQLAlchemyError as e:
            blogger.error(f"[READ JOB-BOARD ERR] JobBoardName: {jname}:: {e}")
            raise GetError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def get_all_jobBoards(self) -> List[JobBoard]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[READ JOB-BOARD ERR] :: {e}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def add_job_board(self, board_data:dict) -> JobBoard:
        try:
            return self.repository.add(**board_data)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT JOB-BOARD ERR] JobBoardName: {board_data['name']}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error occurred while inserting Job Board")
    

    def update_job_board(self, id:int, board_data:dict) -> JobBoard:
        try:
            jboard = self.get_job_board(id)
            if not jboard:
                raise GetError(f"Job Board with id: {id} does not exist")
            return self.repository.update(id, **board_data)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE JOB-BOARD ERR] JobBoardId: {id}:: {e}")
            raise UpdateError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while updating Job Board")
        
    
    def delete_job_board(self, id:int) -> JobBoard:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE JOB-BOARD ERR] JobBoardId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting Job Board")
        
    
    def delete_all_jobBoards(self) -> JobBoard:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE JOB-BOARD ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting all Job Boards")
        