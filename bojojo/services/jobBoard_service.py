from typing import List
import inject
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, DeleteError, GetError, UpdateError
from bojojo.models.Job_Board import JobBoard
from bojojo.repositories.JobBoard_Repo import JobBoardRepository
from sqlalchemy.exc import SQLAlchemyError

from bojojo.utils.bologger import Blogger

class JobBoardService:
    

    repository = inject.attr(JobBoardRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        pass

    
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
            print(self.repository.session)
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
        
    
    def delete_job_board(self, id:int) -> JobBoard:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-BOARD ERR] JobBoardId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_all_jobBoards(self) -> JobBoard:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE JOB-BOARD ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        