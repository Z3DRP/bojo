from loguru import logger
from pathlib import Path
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "bojojo.log"
logger.add(LOG_FILE, rotation="1 MB")

class Blogger:
    def __init__(self):
        self.blogger = logger.bind(name='bojoLogger')
        self.blogger.add(
            LOG_FILE, 
            format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}",
            rotation="1 MB"
        )

    
    def debug(self, msg:str):
        self.blogger.debug(msg)

    
    def info(self, msg:str):
        self.blogger.info(msg)

    
    def warning(self, msg:str):
        self.blogger.warning(msg)

    
    def error(self, msg:str):
        self.blogger.error(msg)

    
    def critical(self, msg:str):
        self.blogger.critical(msg)

    
