from typing import List
import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.base_repo.repository import Repository
from bojojo.models.Completed_Run import CompletedRun

class CompletedRunRepository(Repository):


    session = inject.attr(Session)
    def __init__(self):
        pass
    

    def get(self, id: int) -> CompletedRun:
        try:
            return self.session.execute(select(CompletedRun).where(CompletedRun.id==id)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getAll(self) -> List[CompletedRun]:
        try:
            return self.session.execute(select(CompletedRun)).scalars().all()
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, crun:dict) -> CompletedRun:
        try:
            new_completedRun = self.session.execute(
                insert(CompletedRun)
                .values(**crun)
                .returning(CompletedRun)
            )
            return new_completedRun
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id:int, crun:dict) -> CompletedRun:
        try:
            results = self.session.execute(
                update(CompletedRun)
                .where(CompletedRun.id==id)
                .values(**crun)
                .returning(CompletedRun)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id: int) -> CompletedRun:
        try:
            result = self.session.execute(delete(CompletedRun).where(CompletedRun.id==id).returning(CompletedRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def deleteAll(self) -> CompletedRun:
        try:
            result = self.session.execute(delete(CompletedRun).returning(CompletedRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e