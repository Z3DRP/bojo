from loguru import logger
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "bojojo.log"
logger.add(LOG_FILE, rotation="1 MB")