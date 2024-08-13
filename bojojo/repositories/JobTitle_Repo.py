from typing import List
from sqlalchemy import ChunkedIteratorResult, delete, insert, select, update
from sqlalchemy import ChunkedIteratorResult, delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models.Job_Title import JobTitle
from bojojo.utils.db_session import DbSession


class JobTitleRepository(Repository):


    # session = inject.attr(DbSession)
    def __init__(self, session:Session):
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
            nw_jobTitle = JobTitle(**jobtitle)
            self.session.add(nw_jobTitle)
            self.session.commit()
            # ins = insert(JobTitle).values(**jobtitle).returning(JobTitle)
            # nw_jobTitle = self.session.execute(ins)
            # self.session.commit()
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
            )
            self.session.execute(updtStmnt)
            self.session.commit()
            updtrow = select(JobTitle).where(JobTitle.id==id)
            nw_row = self.session.execute(updtrow).scalars().first()
            return nw_row
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update_by_name(self, name:str, jobtitle:dict) -> JobTitle:
        try:
            updtStmt = (
                update(JobTitle)
                .where(JobTitle.name.in_([name]))
                .values(**jobtitle)
            )
            self.session.execute(updtStmt)
            self.session.commit()
            updtrow = select(JobTitle).where(JobTitle.name==name)
            rslt = self.session.execute(updtrow).scalars().first()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id:int) -> int:
        try:
            dltstmt = delete(JobTitle).where(JobTitle.id==id)
            # return type from session for deletes is diff
            rslt:ChunkedIteratorResult = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete_by_name(self, name:str) -> int:
        try:
            dltStmt = delete(JobTitle).where(JobTitle.name==name)
            rslt:ChunkedIteratorResult = self.session.execute(dltStmt)
            self.session.commit()
            # rslt_count = sum(chunk.rowcount for chunk in rslt.partitions())
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
                    

    def deleteAll(self) -> int:
        try:
            dltstmt = delete(JobTitle)
            rslt:ChunkedIteratorResult = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e