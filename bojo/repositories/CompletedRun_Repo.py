from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojo.base_repo.repository import Repository
from bojo.models.Completed_Run import CompletedRun

class CompletedRunRepository(Repository):


    # session = inject.attr(Session)
    def __init__(self, session:Session):
        self.session = session
    

    def get(self, id: int) -> CompletedRun:
        try:
            rslt = self.session.execute(select(CompletedRun).where(CompletedRun.id==id)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getAll(self) -> List[CompletedRun]:
        try:
            rslt = self.session.execute(select(CompletedRun)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def add(self, crun:dict) -> CompletedRun:
        try:
            nw_run = CompletedRun(**crun)
            self.session.add(nw_run)
            self.session.commit()
            return nw_run
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id:int, crun:dict) -> CompletedRun:
        try:
            updtstmt = (
                update(CompletedRun)
                .where(CompletedRun.id==id)
                .values(**crun)
            )
            self.session.execute(updtstmt)
            self.session.commit()
            updtrow = select(CompletedRun).where(CompletedRun.id==id)
            nw_crun = self.session.execute(updtrow).scalars().first()
            return nw_crun
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id: int) -> int:
        try:
            dltstmt = delete(CompletedRun).where(CompletedRun.id==id)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> int:
        try:
            dltstmt = delete(CompletedRun)
            rslt = self.session.execute(dltstmt)
            self.session.commit()
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e