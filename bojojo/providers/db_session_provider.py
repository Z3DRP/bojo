
import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bojojo import CONFIG_DIR_PATH, db_path
from bojojo.utils.config_reader import get_db_path


def session_provider():
    db_url = f"sqlite:///{db_path()}"
    engine = create_engine(db_url, echo=True)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()