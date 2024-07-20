from typing import List
from injector import inject
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Completed_Run import CompletedRun
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from bojojo.repositories.CompletedRun_Repo import CompletedRunRepository
from bojojo.utils import Blogger as blogger
class CompletedRunService:

    @inject
    def __init__(self, repo:CompletedRunRepository):
        self.repository = repo

    
    def get_completed_run(self, id:int) -> CompletedRun:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            blogger.error(f"[READ COMPLETED-RUN ERR] CompletedRunId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def get_all_completedRuns(self) -> List[CompletedRun]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[READ COMPLETED-RUN ERR]:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
        
    
    def add_completed_run(self, run_data:dict) -> CompletedRun:
        try:
            return self.repository.add(**run_data)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT COMPLETED-RUN ERR] CompletedRun:: {e}")
            raise AddError(DB_WRITE_ERROR, f"DB-ERROR: An error ocurred while inserting completed run")
        
    
    def update_completed_run(self, id:int, run_data:dict) -> CompletedRun:
        try:
            cmpRun = self.get_completed_run(id)
            if not cmpRun:
                raise GetError(f"Completed Run with id:{id} does not exist")
            return self.repository.update(id, **run_data)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE COMPLETED-RUN ERR] CompletedRunId: {id}:: {e}")
            raise UpdateError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while updating completed run")
        
    
    def delete_completed_run(self, id:int) -> CompletedRun:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE COMPLETED-RUN ERR] CompletedRunId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting completed run")
        
    
    def delete_all_completedRuns(self) -> CompletedRun:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE COMPLETED-RUN ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting all completed runs")