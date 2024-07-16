from pathlib import Path
from adapters import DbResponse
from injector import inject
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, AddError, DeleteError, GetError, UpdateError
from bojojo.adapters import CurrentItem, DbResponse
from bojojo.services import ApplicationService, CompletedRunService, JobBoardService, JobTitleService, ResumeService, ScheduledRunService

class DbHandler:


    @inject
    def __init__(self, db_path: Path, appService: ApplicationService, completedRunService: CompletedRunService, jobBoardService: JobBoardService,
                 jobTitleService: JobTitleService, resumeService: ResumeService, scheduledRunService: ScheduledRunService) -> None:
        self.__db_path = db_path
        self.appService = appService
        self.completedRunService = completedRunService
        self.jobBoardService = jobBoardService
        self.jobTitleService = jobTitleService
        self.resumeService = resumeService
        self.scheduledRunService = scheduledRunService

    
    def read_all_applications(self):
        try:
            apps = self.appService.get_all_applications()
            try:
                return DbResponse(self.get_list_response(apps), SUCCESS)
            except:
                return [[], JSON_ERROR]
        except GetError:
            return DbResponse([], DB_READ_ERROR)
        

    def read_application(self, id: int):
        try:
            app = self.appService.get_application(id)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return DbResponse([], JSON_ERROR)
        except GetError:
            return DbResponse([], DB_READ_ERROR)
    

    def write_applications(self, app_data:dict):
        try:
            app = self.appService.add_application(app_data)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return DbResponse([], JSON_ERROR)
        except AddError:
            return DbResponse([], DB_WRITE_ERROR)
        
    
    def update_application(self, app_data:dict):
        try:
            app = self.appService.update_application(app_data)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return DbResponse([], JSON_ERROR)
        except UpdateError:
            return DbResponse([], DB_UPDATE_ERROR)
        
    
    def delete_application(self, id:int):
        try:
            app = self.appService.delete_application(id)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return DbResponse([], JSON_ERROR)
        except DeleteError:
            return DbResponse([], DB_DELETE_ERROR)

    
    def get_list_response(self, item_list):
        responseList = []
        for item in item_list:
            responseList.append(item.__dict__)
        return responseList


    def get_response(app):
        return [app.__dict__]

    