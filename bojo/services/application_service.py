
from typing import List
import inject
from bojojo.base_service import Service
from bojojo.models import Application
from bojojo.repositories.Application_Repo import ApplicationRepository
from sqlalchemy.exc import SQLAlchemyError
from bojojo.utils.bologger import Blogger
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError
from bojojo.utils.repo_injector import create_repo


class ApplicationService(Service):
    
    # repository = inject.attr(ApplicationRepository)
    blogger = inject.attr(Blogger)
    def __init__(self) -> None:
        self.repository = create_repo(repo_type=ApplicationRepository)

    
    def get_application(self, id: int) -> Application:
        try:
            return self.repository.get(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ APPLICATION ERR] ApplicationId: {id}:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_all_applications(self) -> List[Application]:
        try:
            return self.repository.getAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ APPLICATION ERR]:: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        
    
    def get_application_byName(self, name:str) -> Application:
        try:
            return self.repository.get_by_name(name)
        except SQLAlchemyError as e:
            self.blogger.error(f"[READ APPLICATION ERR] ApplicationName: {name} :: {e}")
            raise GetError(DB_READ_ERROR, e._message)
        

    def add_application(self, application_data:dict) -> Application:
        try: 
            return self.repository.add(application_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[INSERT APPLICATION ERR] Company: {application_data['company']}")
            raise AddError(DB_WRITE_ERROR, e._message)


    def update_application(self, id:int, application_data:dict) -> Application:
        try:
            application = self.get_application(id)
            if not application:
                raise GetError(f"Application with id:{id} does not exist")
            return self.repository.update(id, application_data)
        except SQLAlchemyError as e:
            self.blogger.error(f"[UPDATE APPLICATION ERR] ApplicationId: {id}:: {e}" )
            raise UpdateError(DB_UPDATE_ERROR, e._message)

    
    def delete_application(self, id:int) -> int:
        try:
            return self.repository.delete(id)
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE APPLICATION ERR] ApplicationId: {id}:: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)
        
    
    def delete_all_applications(self) -> int:
        try:
            return self.repository.deleteAll()
        except SQLAlchemyError as e:
            self.blogger.error(f"[DELETE APPLICATION ALL ERR] :: {e}")
            raise DeleteError(DB_DELETE_ERROR, e._message)