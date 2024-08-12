from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models.Job_Title import JobTitle
from bojojo.utils.db_session import DbSession


class JobTitleRepository(Repository):


    # session = inject.attr(DbSession)
    def __init__(self, session):
        self.session = session


    def get(self, id:int) -> JobTitle:
        try:
            rslt = self.session.execute(select(JobTitle).where(JobTitle.id==id)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getByName(self, title:str) -> JobTitle:
        try:
            rslt = self.session.execute(select(JobTitle).where(JobTitle.name==title)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getAll(self) -> List[JobTitle]:
        try:
            rslt = self.session.execute(select(JobTitle)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def add(self, jobtitle:dict) -> JobTitle:
        try:
            # nw_jobTitle = JobTitle(**jobtitle)
            # self.session.add(nw_jobTitle)
            # self.session.commit()
            ins = insert(JobTitle).values(**jobtitle).returning(JobTitle)
            nw_jobTitle = self.session.execute(ins)
            self.session.commit()
            return nw_jobTitle
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        

    def update(self, id:int, jobtitle:dict) -> JobTitle:
        try:
            updtStmnt = (
                update(JobTitle)
                .where(JobTitle.id==id)
                .values(**jobtitle)
                .returning(JobTitle)
            )
            rslt = self.session.execute(updtStmnt)
            self.session.flush()
            self.session.commit()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update_by_name(self, name:str, jobtitle:dict) -> JobTitle:
        try:
            updtStmt = (
                update(JobTitle)
                .where(JobTitle.name.in_([name]))
                .values(**jobtitle)
                .returning(JobTitle)
            )
            rslt = self.session.execute(updtStmt)
            self.session.flush()
            self.session.commit()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id:int) -> JobTitle:
        try:
            result = self.session.execute(delete(JobTitle).where(JobTitle.id==id).returning(JobTitle))
            self.session.flush()
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e
        
    
    def delete_by_name(self, name:str) -> JobTitle:
        try:
            dltStmt = delete(JobTitle).where(JobTitle.name.in_([name])).returning(JobTitle)
            rslt = self.session.execute(dltStmt)
            self.session.flush()
            self.session.commit()
            return rslt
        except SQLAlchemyError as e:
            raise e
                    

    def deleteAll(self) -> JobTitle:
        try:
            result = self.session.execute(delete(JobTitle).returning(JobTitle))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e