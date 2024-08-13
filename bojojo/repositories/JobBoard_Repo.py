from typing import List
import inject
from sqlalchemy import ChunkedIteratorResult, delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models.Job_Board import JobBoard


class JobBoardRepository(Repository):


    # session = inject.attr(Session)
    def __init__(self, session:Session):
        self.session = session

    
    def get(self, id: int) -> JobBoard:
        try:
            rslt = self.session.execute(select(JobBoard).where(JobBoard.id==id)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getByName(self, jname:str) -> JobBoard:
        try:
            rslt = self.session.execute(select(JobBoard).where(JobBoard.name==jname)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getAll(self) -> List[JobBoard]:
        try:
            rslt = self.session.execute(select(JobBoard)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def add(self, board:dict) -> JobBoard:
        try:
            # nw_jobboard = self.session.execute(
            #     insert(JobBoard)
            #     .values(**board)
            #     .returning(JobBoard)
            # ).fetchone()
            nw_jb = JobBoard(**board)
            self.session.add(nw_jb)
            self.session.commit()
            return nw_jb
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id: int, board:dict) -> JobBoard:
        try:
            updtstmnt = (
                update(JobBoard)
                .where(JobBoard.id==id)
                .values(**board)
            )
            self.session.execute(updtstmnt)
            self.session.commit()
            updtrow = select(JobBoard).where(JobBoard.id==id)
            rslt = self.session.execute(updtrow).scalars().first()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        

    def update_by_name(self, name:str, board:dict) -> JobBoard:
        try:
            updtstmt = (
                update(JobBoard)
                .where(JobBoard.name==name)
                .values(**board)
            )
            self.session.execute(updtstmt)
            self.session.commit()
            updtrow = select(JobBoard).where(JobBoard.name==name)
            rslt = self.session.execute(updtstmt).scalars().first()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id: int) -> int:
        try:
            dltstmt = delete(JobBoard).where(JobBoard.id==id)
            rslt:ChunkedIteratorResult = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete_by_name(self, name:str) -> int:
        try:
            dltstmt = delete(JobBoard).where(JobBoard.name==name)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        

    def deleteAll(self) -> int:
        try:
            dltstmt = delete(JobBoard)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e