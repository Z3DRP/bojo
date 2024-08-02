from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Scheduled_Run import ScheduledRun
from bojojo.repositories import repository


class ScheduledRunRepository(repository):


    session = inject.attr(Session)
    def __init__(self, session: Session):
        pass

    
    def get(self, id: int) -> ScheduledRun:
        try:
            return self.session.execute(select(ScheduledRun).where(ScheduledRun.id==id)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getAll(self) -> List[ScheduledRun]:
        try:
            return self.session.execute(select(ScheduledRun)).scalars().all()
        except SQLAlchemyError as e:
            raise e
        
    
    def getByName(self, name:str) -> ScheduledRun:
        try:
            return self.session.execute(select(ScheduledRun).where(ScheduledRun.name==name).returning(ScheduledRun)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, **kwargs) -> ScheduledRun:
        try:
            nw_run = self.session.execute(
                insert(ScheduledRun)
                .values(**kwargs)
                .returning(ScheduledRun)
            )
            self.session.commit()
            return nw_run
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, name:str, **kwargs) -> ScheduledRun:
        try:
            results = self.session.execute(
                update(ScheduledRun)
                .where(ScheduledRun.name==name)
                .values(**kwargs)
                .returning(ScheduledRun)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id:int) -> ScheduledRun:
        try:
            result = self.session.execute(delete(ScheduledRun).where(ScheduledRun.id==id).returning(ScheduledRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete_byName(self, name:str) -> ScheduledRun:
        try:
            result = self.session.execute(delete(ScheduledRun).where(ScheduledRun.name==name).returning(ScheduledRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> ScheduledRun:
        try:
            result = self.session.execute(delete(ScheduledRun).returning(ScheduledRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e