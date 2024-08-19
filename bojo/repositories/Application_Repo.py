from typing import Any, List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojo.base_repo.repository import Repository
from bojo.models import Application


class ApplicationRepository(Repository):

    # session = inject.attr(Session)
    def __init__(self, session:Session):
        self.session = session


    def get(self, id: int) -> Application:
        try:
            rslt = self.session.execute(select(Application).where(Application.id==id)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def get_by_name(self, name:str) -> Application:
        try:
            rslt = self.session.execute(select(Application).where(Application.name==name)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    
    def getAll(self) -> List[Application]:
        try:
            rslt = self.session.execute(select(Application)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def add(self, application:dict) -> Application:
        try:
            nw_app = Application(**application)
            self.session.add(nw_app)
            self.session.commit()
            return nw_app
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id:int, application:dict) -> Application:
        try:
            updtstmt = (
                update(Application)
                .where(Application.id==id)
                .value(**application)
            )
            self.session.execute(updtstmt)
            self.session.commit()
            updtrow = select(Application)
            nw_row = self.session.execute(updtrow).scalars().first()
            return nw_row
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e


    def delete(self, id: int ) -> int:
        try:
            dltstmt = delete(Application).where(Application.id==id)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> int:
        try:
            dltstmt = delete(Application)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e