"""TOP-LEVEL package for Scrappy web scrapper"""
#wbscrapper/__init__.py

__app_name__ = "bojo"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    DB_UPDATE_ERROR,
    DB_DELETE_ERROR,
    DB_CREATE_ERROR,
    JSON_ERROR,
    ID_ERROR,
    FILE_PATH_ERROR,
) = range(11)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    DB_CREATE_ERROR: "database creation error",
    DB_UPDATE_ERROR: "database update error",
    DB_DELETE_ERROR: "database delete error",
    JSON_ERROR: "json parsing error",
    ID_ERROR: "bojo id error",
    FILE_PATH_ERROR: "file path does not exist"
}

class RepoException(Exception):
    """Base clas for all repo errors"""
    def __init__(self, errCode, msg):
        self.err_code = errCode
        self.message = msg

class AddError(RepoException):
    """Exception raised for errors durring add operation"""
    pass

class GetError(RepoException):
    """Exception raise for get operations"""
    pass

class UpdateError(RepoException):
    """Exception raised for update operations"""
    pass

class DeleteError(RepoException):
    """Exception raised for delete error"""
    pass
