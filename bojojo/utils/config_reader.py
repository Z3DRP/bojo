import configparser
from pathlib import Path
from bojojo import CONFIG_DIR_PATH


def get_db_path():
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_DIR_PATH)
    return Path(config_parser["General"]["database"])