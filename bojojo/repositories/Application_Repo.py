from typing import Any, List
from injector import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Application
from bojojo.repositories import repository


class ApplicationRepository(repository):
    @inject
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
        
    
    def add(self, **kwargs) -> Application:
        try:
            new_application = self.session.execute(
                insert(Application).values(**kwargs)
                .returning(Application)
            )
            self.session.commit()
            return new_application
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id:int, **kwargs) -> Application:
        try:
            results = self.session.execute(
                update(Application)
                .where(Application.id==id)
                .values(**kwargs)
                .returning(Application)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e


    def delete(self, id: int ) -> Application:
        try:
            result = self.session.execute(delete(Application).where(Application.id==id).returning(Application))
            self.session.comit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e