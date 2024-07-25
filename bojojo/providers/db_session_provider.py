
import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bojojo import CONFIG_DIR_PATH
from bojojo.utils.config_reader import get_db_path


def session_provider():
    db_path = get_db_path()
    engine = create_engine(db_path)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autofulsh=False, bind=engine))
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()