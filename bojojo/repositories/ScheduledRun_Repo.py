from typing import List
from injector import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Scheduled_Run import ScheduledRun
from bojojo.repositories import repository


class ScheduledRunRepository(repository):

    @inject
    def __init__(self, session: Session):
        self.session = session    

    
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
        
    
    def update(self, id:int, **kwargs) -> ScheduledRun:
        try:
            results = self.session.execute(
                update(ScheduledRun)
                .where(ScheduledRun.id==id)
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