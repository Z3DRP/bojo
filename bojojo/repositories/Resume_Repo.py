import sqlite3
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo import DB_WRITE_ERROR, AddError
from bojojo.models import Resume
from bojojo.repositories import repository
from bojojo.repositories import db_init
from bojojo.utils import bologger as blogger

class ResumeRepository(repository):


    def __init__(self, session: Session):
        self.session = session

    
    def add(self, resume: Resume):
        try:
            self.session.add(resume)
            self.session.commit()
            blogger.info(f"Resume added: [id: {resume.id}, jobTitleId: {resume.job_title_id}]")
            return resume
        except SQLAlchemyError as e:
            self.session.rollback()
            # needs to be changed to log error and return err code
            blogger.error(f"ERROR: Exception occurred inserting resume {resume.id}:: [{e}]")
            #NOTE then in the cli i can grab this error code and use it like
            #except error as e: -> e.code, e.message
            raise AddError(DB_WRITE_ERROR, e)
