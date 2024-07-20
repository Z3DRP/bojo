
from typing import List

from injector import inject
from bojojo.models import Application
from bojojo.repositories.Application_Repo import ApplicationRepository
from sqlalchemy.exc import SQLAlchemyError
from bojojo.utils import Blogger as blogger
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError


class ApplicationService:
    
    @inject
    def __init__(self, repo: ApplicationRepository):
        self.repository = repo

    
    def get_application(self, id: int) -> Application:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            blogger.error(f"[READ ERR] ApplicationId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, "DB-Error: An error ocurred while reading")
        
    
    def get_all_applications(self) -> List[Application]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            blogger.error(f"[READ ERR]:: {e}")
            raise GetError(DB_READ_ERROR, "DB-ERROR: An error ocurred while reading")

        
    def add_application(self, application_data:dict) -> Application:
        try: 
            return self.repository.add(**application_data)
        except SQLAlchemyError as e:
            blogger.error(DB_WRITE_ERROR, f"[INSERT APPLICATION ERR] Company: {application_data['company']}")
            raise AddError(f"DB-Error: An error ocurred while inserting application")


    def update_application(self, id:int, application_data:dict) -> Application:
        try:
            application = self.get_application(id)
            if not application:
                raise GetError(f"Application with id:{id} does not exist")
            return self.repository.update(id, **application_data)
        except SQLAlchemyError as e:
            blogger.error(f"[UPDATE APPLICATION ERR] ApplicationId: {id}:: {e}" )
            raise UpdateError(DB_WRITE_ERROR, "DB-ERROR: An error ocurred while updating Application")

    
    def delete_application(self, id:int) -> Application:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE APPLICATION ERR] ApplicationId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, f"DB-ERROR: An error ocurred while deleting application")
        
    
    def delete_all_applications(self) -> Application:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            blogger.error(f"[DELETE APPLICATION ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, "DB-ERROR: An error ocurred while deleting all applications")
        