"""
db_config.py
This module provides sqlite db initialization
"""
import configparser
from pathlib import Path
from bojojo import DB_WRITE_ERROR, DB_CREATE_ERROR, SUCCESS
from bojojo.repositories import db_init as db
from bojojo import DEFAULT_DB_FILE_PATH

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the bojo database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create bojo database and tables"""
    try:
        db.initialize_db(db_path)
    except Exception:
        return DB_CREATE_ERROR
    return SUCCESS
    
    