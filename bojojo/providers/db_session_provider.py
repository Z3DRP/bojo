
import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bojojo import CONFIG_DIR_PATH


def session_provider():
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_DIR_PATH)
    db_path = Path(config_parser["General"]["database"])
    engine = create_engine(db_path)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autofulsh=False, bind=engine))
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()