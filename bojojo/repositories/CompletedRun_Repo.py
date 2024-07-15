from typing import List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.repositories import repository
from bojojo.models.Completed_Run import CompletedRun

class CompletedRunRepository(repository):


    def __init__(self, session: Session):
        self.session = session    


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
        
    
    def add(self, completedRun: CompletedRun) -> CompletedRun:
        try:
            new_completedRun = self.session.execute(
                insert(CompletedRun)
                .values(
                    execution_date=completedRun.execution_date,
                    start=completedRun.start,
                    finish=completedRun.finish,
                    failed_submission=completedRun.failed_submissions,
                    run_id=completedRun.run_id
                )
                .returning(CompletedRun)
            )
            return new_completedRun
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, completedRun: CompletedRun) -> CompletedRun:
        try:
            results = self.session.execute(
                update(CompletedRun)
                .where(CompletedRun.id==completedRun.id)
                .values(
                    execution_date=completedRun.execution_date,
                    start=completedRun.start,
                    finish=completedRun.finish,
                    failed_submissions=completedRun.failed_submissions,
                    run_id=completedRun.run_id
                )
                .returning(CompletedRun)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, completedRun: CompletedRun) -> CompletedRun:
        try:
            result = self.session.execute(delete(CompletedRun).where(CompletedRun.id==completedRun.id).returning(CompletedRun))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e