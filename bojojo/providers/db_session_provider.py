
import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bojojo import CONFIG_DIR_PATH, DB_URL, db_path
from bojojo.base_model.base_model import init_db_models
from bojojo.utils.config_reader import get_db_path


def get_engine():
    engine = create_engine(DB_URL, echo=True)
    init_db_models(engine)
    return engine


def session_provider():
    engine = get_engine()
    sess = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = sess()
    return db