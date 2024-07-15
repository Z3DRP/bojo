from typing import List
from sqlalchemy.exc import SQLAlchemyError
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from bojojo.models.Scheduled_Run import ScheduledRun
from bojojo.repositories.ScheduledRun_Repo import ScheduledRunRepository
from bojojo.utils import Blogger as blogger

class ScheduledRunService:

    def __init__(self, repo: ScheduledRunRepository):
        self.repository = repo
    
    def get_scheduled_run(self, id:int) -> ScheduledRun:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            blogger.error(f"[READ SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
    

    def get_all_scheduledRuns(self) -> List[ScheduledRun]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[READ SCHEDULED-RUN ERR]:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")
    

    def add_scheduled_run(self, run_data:dict) -> ScheduledRun:
        try:
            return self.repository.add(**run_data)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise AddError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while inserting Scheduled Run")
    

    def update_scheduled_run(self, id:int, run_data:dict) -> ScheduledRun:
        try:
            schRun = self.get_scheduled_run(id)
            if not schRun:
                raise GetError(f"Scheduled Run with id:{id} does not exist")
            return self.repository.update(id, **run_data)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise UpdateError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while updating Scheduled Run")
        
    
    def delete_scheduled_run(self, id:int) -> ScheduledRun:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting Scheduled Run")