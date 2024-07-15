import sqlite3
from typing import List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Resume
from bojojo.repositories import repository
from bojojo.repositories import db_init

class ResumeRepository(repository):


    #TODO possibly change this setup, remove AddError exceptions out into the
    #service class that will use this repository....
    def __init__(self, session: Session):
        self.session = session


    def get(self, rid: int) -> Resume:
        try:
            result = self.session.execute(select(Resume).where(Resume.id==rid)).scalars().first()
            return result
        except SQLAlchemyError as e:
            raise e
        
    def getAll(self) -> List[Resume]:
        try:
            results = self.session.execute(select(Resume)).scalars().all()
            return results
        except SQLAlchemyError as e:
            raise e

    
    def add(self, resume: Resume) -> Resume:
        try:
            nw_resume = self.session.execute(insert(Resume).values(job_title_id=resume.job_title_id, file_path=resume.file_path).returning(Resume))
            self.session.commit()
            return nw_resume
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    
    def update(self, resume: Resume) -> Resume:
        try:
            results = self.session.execute(
                update(Resume)
                .where(Resume.id==resume.id)
                .values(job_title_id=resume.job_title_id, file_path=resume.file_path)
                .returning(Resume)
            )
            self.session.commit()
            return results
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    def update_path(self, resume_id: int, file_path: str) -> Resume:
        try:
            result = self.session.execute(
                update(Resume)
                .where(Resume.id==resume_id)
                .values(file_path=file_path)
                .returning(Resume)
            )
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    def update_job_title(self, resume_id: int, job_title_id: int) -> Resume:
        try:
            result = self.session.execute(
                update(Resume)
                .where(Resume.id==resume_id)
                .values(job_title_id=job_title_id)
                .returning(Resume)
            )
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
    
    def update_name(self, resume_id: int, name: str) -> Resume:
        try:
            result = self.session.execute(
                update(Resume)
                .where(Resume.id==resume_id)
                .values(name=name)
                .returning(Resume)
            )
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
        
    def delete(self, resume: Resume) -> Resume:
        try:
            result = self.session.execute(delete(Resume).where(Resume.id==resume.id).returning(Resume))
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
