from typing import List
from injector import inject
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models.Job_Title import JobTitle
from bojojo.repositories import repository


class JobTitleRepository(repository):

    @inject
    def __init__(self, session: Session):
        self.session = session    

    
    def get(self, id:int) -> JobTitle:
        try:
            return self.session.execute(select(JobTitle).where(JobTitle.id==id)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getByName(self, title:str) -> JobTitle:
        try:
            return self.session.execute(select(JobTitle).where(JobTitle.name==title)).scalars().first()
        except SQLAlchemyError as e:
            raise e
        
    
    def getAll(self) -> List[JobTitle]:
        try:
            return self.session.execute(select(JobTitle)).scalars().all()
        except SQLAlchemyError as e:
            raise e
        
    
    def add(self, **kwargs) -> JobTitle:
        try:
            nw_jobTitle = self.session.execute(
                insert(JobTitle)
                .values(**kwargs)
                .returning(JobTitle)
            )
            self.session.commit()
            return nw_jobTitle
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        

    def update(self, id:int, **kwargs) -> JobTitle:
        try:
            results = self.session.execute(
                update(JobTitle)
                .where(JobTitle.id==id)
                .values(**kwargs)
                .returning(JobTitle)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def delete(self, id:int) -> JobTitle:
        try:
            result = self.session.execute(delete(JobTitle).where(JobTitle.id==id).returning(JobTitle))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e
            

    def deleteAll(self) -> JobTitle:
        try:
            result = self.session.execute(delete(JobTitle).returning(JobTitle))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            raise e