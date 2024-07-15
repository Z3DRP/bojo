from typing import List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Application
from bojojo.repositories import repository


class ApplicationRepository(repository):

    def __init__(self, session: Session):
        self.session = session


    def get(self, id: int) -> Application:
        try:
            result = self.session.execute(select(Application).where(Application.id==id)).scalars().first()
            return result
        except SQLAlchemyError as e:
            raise e

    
    def getAll(self) -> List[Application]:
        try:
            results = self.session.execute(select(Application)).scalars().all()
            return results
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, application: Application) -> Application:
        try:
            new_application = self.session.execute(
                insert(Application).values(
                    company=application.company,
                    job_title=application.job_title,
                    location=application.location,
                    pay=application.pay,
                    apply_date=application.apply_date,
                    submitted_successfully=application.submitted_successfully,
                    run_id=application.run_id
                )
                .returning(Application)
            )
            self.session.commit()
            return new_application
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, application: Application) -> Application:
        try:
            results = self.session.execute(
                update(Application)
                .where(Application.id==application.id)
                .values(
                    company=application.company,
                    job_title=application.job_title,
                    location=application.location,
                    pay=application.pay,
                    apply_date=application.apply_date,
                    submitted_successfully=application.submitted_successfully,
                    run_id=application.run_id
                )
                .returning(Application)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e


    def delete(self, application: Application) -> Application:
        try:
            result = self.session.execute(delete(Application).where(Application.id==application.id).returning(Application))
            self.session.comit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e