
from typing import List
from bojojo.models import Application
from bojojo.repositories.Application_Repo import ApplicationRepository
from sqlalchemy import 
from sqlalchemy.exc import SQLAlchemyError
from bojojo.utils import Blogger as blogger
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR, AddError, GetError, UpdateError, DeleteError


class ApplicationService:
    
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

        
    def add_application(self, application: Application):
        try: 
            application = Application(
                comapny=application.comapny,
                job_title=application.job_title,
                location=application.location,
                pay=application.pay,
                apply_date=application.apply_date,
                submitted_successfully=application.submitted_successfully,
                run_id=application.run_id
            )
            return self.repository.add(application)
        except SQLAlchemyError as e:
            blogger.error(f"[INSERT APPLICATION ERR] Company: {application.company}")
            raise AddError(f"DB-Error: An error ocurred while inserting application")
