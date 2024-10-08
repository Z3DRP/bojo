from typing import List
import inject
from sqlalchemy.exc import SQLAlchemyError
from bojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from bojo.base_service import Service
from bojo.models.Scheduled_Run import ScheduledRun
from bojo.repositories.ScheduledRun_Repo import ScheduledRunRepository
from bojo.types.schedule_types import ScheduleType
from bojo.utils.bologger import Blogger
from bojo.utils.repo_injector import create_repo

class ScheduledRunService(Service):

    
    # repository = inject.attr(ScheduledRunRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        self.repository = create_repo(repo_type=ScheduledRunRepository)

    
    def get_scheduled_run(self, id:int) -> ScheduledRun:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
    

    def get_all_scheduledRuns(self) -> List[ScheduledRun]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ SCHEDULED-RUN ERR]:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_scheduledRun_by_type(self, type:ScheduleType) -> List[ScheduledRun]:
        try:
            return self.repository.getByType(type)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ SCHEDULED-RUN ERR]:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_scheduledRunByName(self, name:str) -> ScheduledRun:
        try:
            return self.repository.getByName(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ SCHEDULED-RUN ERR]:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
    

    def add_scheduled_run(self, run_data:dict) -> ScheduledRun:
        try:
            return self.repository.add(**run_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise AddError(DB_WRITE_ERROR, e._message)
    

    def update_scheduled_run(self, name:str, run_data:dict) -> ScheduledRun:
        try:
            schRun = self.get_scheduled_run(name)
            if not schRun:
                raise GetError(f"Scheduled Run with name:{name} does not exist")
            return self.repository.update(name, **run_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise UpdateError(DB_UPDATE_ERROR, e._message)
        
    
    def delete_scheduled_run(self, id:int) -> ScheduledRun:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE SCHEDULED-RUN ERR] ScheduledRunId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_scheduledRun_byName(self, name:str) -> ScheduledRun:
        try:
            return self.repository.delete_byName(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE SCHEDULED-RUN ERR] ScheduledRunName: {name}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
    
    def delete_all_scheduledRuns(self) -> ScheduledRun:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE SCHEDULED-RUN ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)