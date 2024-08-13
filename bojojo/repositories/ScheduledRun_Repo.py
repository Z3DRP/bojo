from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models.Scheduled_Run import ScheduledRun


class ScheduledRunRepository(Repository):


    # session = inject.attr(Session)
    def __init__(self, session:Session):
        self.session = session

    
    def get(self, id: int) -> ScheduledRun:
        try:
            rslt = self.session.execute(select(ScheduledRun).where(ScheduledRun.id==id)).scalars().first()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def getAll(self) -> List[ScheduledRun]:
        try:
            rslt = self.session.execute(select(ScheduledRun)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
                
    
    def getByName(self, name:str) -> ScheduledRun:
        try:
            rslt = self.session.execute(select(ScheduledRun)).scalars().all()
            self.session.close()
            return rslt
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def add(self, srun:dict) -> ScheduledRun:
        try:
            nw_srn = ScheduledRun(**srun)
            self.session.add(nw_srn)
            self.session.commit()
            return nw_srn
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id:int, srun:dict) -> ScheduledRun:
        try:
            updtstmt = (
                update(ScheduledRun)
                .where(ScheduledRun.id==id)
                .values(**srun)
            )
            self.session.execute(updtstmt)
            self.session.commit()
            updtrow = select(ScheduledRun).where(ScheduledRun.id==id)
            nw_sr = self.session.execute(updtrow).scalars().first()
            return nw_sr
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update_by_name(self, name:str, srun:dict) -> ScheduledRun:
        try:
            updstm = (
                update(ScheduledRun)
                .where(ScheduledRun.name==name)
                .values(**srun)
            )
            self.session.execute(updstm)
            self.session.commit()
            updrw = select(ScheduledRun).where(ScheduledRun.name==name)
            nw_sr = self.session.execute(updrw).scalars().first()
            return nw_sr
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id:int) -> int:
        try:
            dltstm = delete(ScheduledRun).where(ScheduledRun.id==id)
            rslt = self.session.execute(dltstm)
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete_byName(self, name:str) -> ScheduledRun:
        try:
            dltstm = delete(ScheduledRun).where(ScheduledRun.name==name)
            rslt = self.session.execute(dltstm)
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> ScheduledRun:
        try:
            dltstm = delete(ScheduledRun)
            rslt = self.session.execute(dltstm)
            return rslt.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e