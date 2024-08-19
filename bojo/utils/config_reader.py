import configparser
from pathlib import Path
from bojo import CONFIG_DIR_PATH, db_path


def get_db_path():
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_DIR_PATH)
    return db_path()