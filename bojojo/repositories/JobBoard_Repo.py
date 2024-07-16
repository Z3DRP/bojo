from typing import List
from injector import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Job_Board import JobBoard
from bojojo.repositories import repository


class JobBoardRepository(repository):

    @inject
    def __init__(self, session: Session):
        self.session = session    

    
    def get(self, id: int) -> JobBoard:
        try:
            return self.session.execute(select(JobBoard).where(JobBoard.id==id)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getAll(self) -> List[JobBoard]:
        try:
            return self.session.execute(select(JobBoard)).scalars().all()
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, **kwargs) -> JobBoard:
        try:
            nw_jobboard = self.session.execute(
                insert(JobBoard)
                .values(**kwargs)
                .returning(JobBoard)
            )
            self.session.commit()
            return nw_jobboard
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update(self, id: int, **kwargs) -> JobBoard:
        try:
            results = self.session.execute(
                update(JobBoard)
                .where(JobBoard.id==id)
                .values(**kwargs)
                .returning(JobBoard)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id: int) -> JobBoard:
        try:
            result = self.session.execute(delete(JobBoard).where(JobBoard.id==id).returning(JobBoard))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e