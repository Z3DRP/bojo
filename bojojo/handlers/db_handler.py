from pathlib import Path
from typing import List
from adapters import DbResponse
import inject
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, AddError, DeleteError, GetError, UpdateError
from bojojo.adapters import CurrentItem, DbResponse
from bojojo.models.Completed_Run import CompletedRun
from bojojo.services import ApplicationService, CompletedRunService, JobBoardService, JobTitleService, ResumeService, ScheduledRunService

class DbHandler:

    appService = inject.atrr(ApplicationService)
    completedRunService = inject.attr(CompletedRunService)
    jobBoardService = inject.attr(JobBoardService)
    jobTitleService = inject.attr(JobTitleService)
    resumeService = inject.attr(ResumeService)
    scheduledRunService = inject.attr(ScheduledRunService)
    
    def __init__(self, db_path: Path) -> None:
        self.__db_path = db_path

    
    def get_path(self):
        return self.__db_path

    
    def read_all_applications(self) -> DbResponse:
        try:
            apps = self.appService.get_all_applications()
            try:
                return DbResponse(self.get_list_response(apps), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        

    def read_application(self, id: int) -> DbResponse:
        try:
            app = self.appService.get_application(id)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_applications(self, app_data:dict) -> DbResponse:
        try:
            app = self.appService.add_application(app_data)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
        
    
    def modify_application(self, app_data:dict) -> DbResponse:
        try:
            app = self.appService.update_application(app_data)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
        
    
    def remove_application(self, id:int) -> DbResponse:
        try:
            app = self.appService.delete_application(id)
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def remove_all_applications(self) -> DbResponse:
        try:
            app = self.appService.delete_all_applications()
            try:
                return DbResponse(self.get_response(app), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def read_completed_run(self, id:int) -> DbResponse:
        try:
            run = self.completedRunService.get_completed_run()
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_all_completedRuns(self) -> DbResponse:
        try:
            runs = self.completedRunService.get_all_completedRuns()
            try:
                return DbResponse(self.get_list_response(runs), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        
    
    def write_completed_run(self, run_data:dict) -> DbResponse:
        try:
            run = self.completedRunService.add_completed_run(run_data)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
    

    def modify_completed_run(self, id:int, run_data:dict) -> DbResponse:
        try:
            run = self.completedRunService.update_completed_run(id, run_data)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
        
    
    def remove_completed_run(self, id:int) -> DbResponse:
        try:
            run = self.completedRunService.delete_completed_run(id)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return DbResponse(DB_DELETE_ERROR)
        
    
    def remove_all_completeRuns(self) -> DbResponse:
        try:
            run = self.completedRunService.delete_all_completedRuns()
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
    

    def read_job_board(self, id:int) -> DbResponse:
        try:
            jobBoard = self.jobBoardService.get_job_board(id)
            try:
                return DbResponse(self.get_response(jobBoard), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        
    
    def read_jobBoard_by_name(self, jname:str) -> DbResponse:
        try:
            jobBoard = self.jobBoardService.get_jobBoard_by_name(jname)
            try:
                return DbResponse(self.get_response(jobBoard), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        
    
    def read_all_jobBoards(self) -> DbResponse:
        try:
            jobBoards = self.jobBoardService.get_all_jobBoards()
            try:
                return DbResponse(self.get_list_response(jobBoards), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_job_board(self, board_data:dict) -> DbResponse:
        try:
            jobBoard = self.jobBoardService.add_job_board(board_data)
            try:
                return DbResponse(self.get_response(jobBoard), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
    

    def modify_job_board(self, id:int, board_data:dict) -> DbResponse:
        try:
            board = self.jobBoardService.update_job_board(id, board_data)
            try:
                return DbResponse(self.get_response(board), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
    

    def remove_job_board(self, id:int) -> DbResponse:
        try:
            board = self.jobBoardService.delete_job_board(id)
            try:
                return DbResponse(self.get_response(board), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def remove_all_jobBoard(self) -> DbResponse:
        try:
            board = self.jobBoardService.delete_all_jobBoards()
            try:
                return DbResponse(self.get_response(board), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
    

    def read_job_title(self, id:int) -> DbResponse:
        try:
            jtitle = self.jobTitleService.get_job_title(id)
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        
    
    def read_job_title_byName(self, title:str) -> DbResponse:
        try:
            jtitle = self.jobTitleService.get_job_title_by_name(title)
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_all_jobTitles(self) -> DbResponse:
        try:
            jtitles = self.jobTitleService.get_all_jobTitles()
            try:
                return DbResponse(self.get_list_response(jtitles), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_job_title(self, job_data:dict) -> DbResponse:
        try:
            jtitle = self.jobTitleService.add(job_data)
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
    
    
    def modify_job_title(self, id:int, job_data:dict) -> DbResponse:
        try:
            jtitle = self.jobTitleService.update_job_title(id, job_data)
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
        
    
    def remove_job_title(self, id:int) -> DbResponse:
        try:
            jtitle = self.jobTitleService.delete_job_title(id)
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def remove_all_jobTitles(self) -> DbResponse:
        try:
            jtitle = self.jobTitleService.delete_all_jobTitles()
            try:
                return DbResponse(self.get_response(jtitle), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)

        
    def read_resume(self, id:int) -> DbResponse:
        try:
            resume = self.resumeService.get_resume(id)
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_all_resumes(self) -> DbResponse:
        try:
            resumes = self.resumeService.get_all_resumes()
            try:
                return DbResponse(self.get_list_response(resumes), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_resume(self, resume_data:dict) -> DbResponse:
        try:
            resume = self.resumeService.add_resume(resume_data)
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
    
    
    def modify_resume(self, id:int, resume_data:dict) -> DbResponse:
        try:
            resume = self.resumeService.update_resume(id, resume_data)
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
        
    
    def remove_resume(self, id:int) -> DbResponse:
        try:
            resume = self.resumeService.delete_resume(id)
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def remove_all_resumes(self) -> DbResponse:
        try:
            resume = self.resumeService.delete_all_resumes()
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
            

    def read_scheduled_run(self, id:int) -> DbResponse:
        try:
            run = self.scheduledRunService.get_scheduled_run(id)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_all_scheduledRuns(self) -> DbResponse:
        try:
            runs = self.scheduledRunService.get_all_scheduledRuns()
            try:
                return DbResponse(self.get_list_response(runs), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_scheduled_run_byName(self, name:str) -> DbResponse:
        try:
            run = self.scheduledRunService.get_scheduledRunByName(name)
            try:
                return DbResponse(self.get_list_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
        

    def write_scheduled_run(self, run_data:dict) -> DbResponse:
        try:
            run = self.scheduledRunService.add_scheduled_run(run_data)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except AddError:
            return self.get_db_err(DB_WRITE_ERROR)
    

    def modify_scheduled_run(self, id:int, run_data:dict) -> DbResponse:
        try:
            run = self.scheduledRunService.update_scheduled_run(id, run_data)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
    

    def remove_scheduled_run(self, id:int) -> DbResponse:
        try:
            run = self.scheduledRunService.delete_scheduled_run(id)
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def remove_scheduledRun_byName(self, name:str) -> DbResponse:
        try:
            run = self.scheduledRunService.delete_scheduledRun_byName()
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
            
    
    def remove_all_scheduledRuns(self) -> DbResponse:
        try:
            run = self.scheduledRunService.delete_all_scheduledRuns()
            try:
                return DbResponse(self.get_response(run), SUCCESS)
            except:
                return self.get_json_err()
        except DeleteError:
            return self.get_db_err(DB_DELETE_ERROR)
        
    
    def get_list_response(self, item_list) -> List[dict]:
        responseList = []
        for item in item_list:
            responseList.append(item.__dict__)
        return responseList


    def get_response(app) -> dict:
        return [app.__dict__]
    
    
    def get_json_err() -> DbResponse:
        return DbResponse([], JSON_ERROR)
    

    def get_db_err(errType:int) -> DbResponse:
        return DbResponse([], errType)

    