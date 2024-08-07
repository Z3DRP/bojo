import sqlite3
from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models import Resume
from bojojo.repositories import db_init

class ResumeRepository(Repository):


    session = inject.attr(Session)
    def __init__(self):
        pass

    def get(self, rid: int) -> Resume:
        try:
            result = self.session.execute(select(Resume).where(Resume.id==rid)).scalars().first()
            return result
        except SQLAlchemyError as e:
            raise e
        
    
    def getByName(self, name:str) -> Resume:
        try:
            return self.session.execute(select(Resume).where(Resume.name==name)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
        
    def getAll(self) -> List[Resume]:
        try:
            results = self.session.execute(select(Resume)).scalars().all()
            return results
        except SQLAlchemyError as e:
            raise e

    
    def add(self, resume:dict) -> Resume:
        try:
            nw_resume = self.session.execute(insert(Resume).values(**resume).returning(Resume))
            self.session.commit()
            return nw_resume
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    
    def update(self, name:str, resume:dict) -> Resume:
        try:
            results = self.session.execute(
                update(Resume)
                .where(Resume.name==name)
                .values(**resume)
                .returning(Resume)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
        
    def delete(self, name:str) -> Resume:
        try:
            result = self.session.execute(delete(Resume).where(Resume.name==name).returning(Resume))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> Resume:
        try:
            result = self.sessin.execute(delete(Resume).returning(Resume))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e
        
