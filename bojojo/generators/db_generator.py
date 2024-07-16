from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DbGenerator:
    def __init__(self, db_path:str):
        self.db_path = db_path
        self.engine = create_engine(self.db_path)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autofulsh=False, bind=self.engine))

    
    def generate_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()