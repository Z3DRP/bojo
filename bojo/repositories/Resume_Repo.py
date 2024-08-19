import sqlite3
from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojo.base_repo.repository import Repository
from bojo.models import Resume
from bojo.repositories import db_init

class ResumeRepository(Repository):


    # session = inject.attr(Session)
    def __init__(self, session:Session):
        self.session = session


    def get(self, rid: int) -> Resume:
        try:
            result = self.session.execute(select(Resume).where(Resume.id==rid)).scalars().first()
            self.session.close()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getByName(self, name:str) -> Resume:
        try:
            rslt = self.session.execute(select(Resume).where(Resume.name==name)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
        
    def getAll(self) -> List[Resume]:
        try:
            rslt = self.session.execute(select(Resume)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    
    def add(self, resume:dict) -> Resume:
        try:
            nw_res = Resume(**resume)
            self.session.add(nw_res)
            self.session.commit()
            return nw_res
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    
    def update(self, id:int, resume:dict) -> Resume:
        try:
            updstmt = (
                update(Resume)
                .where(Resume.id==id)
                .value(**resume)
            )
            self.session.execute(updstmt)
            self.session.commit()
            updrow = select(Resume).where(Resume.id==id)
            nw_row = self.session.execute(updrow).scalars().first()
            return nw_row
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update_by_name(self, name:str, resume:dict) -> Resume:
        try:
            updstmt = (
                update(Resume)
                .where(Resume.name==name)
                .values(**resume)
            )
            self.session.execute(updstmt)
            self.session.commit()
            updrow = select(Resume).where(Resume.name==name)
            rslt = self.session.execute(updrow).scalars().first()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
        
    def delete(self, id:int) -> int:
        try:
            dltstm = delete(Resume).where(Resume.id==id)
            rslt = self.session.execute(dltstm)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete_by_name(self, name:str) -> int:
        try:
            dltstm = delete(Resume).where(Resume.name==name)
            rslt = self.session.execute(dltstm)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> Resume:
        try:
            dltstm = delete(Resume)
            rslt = self.session.execute(dltstm)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
