from pathlib import Path
from typing import List
import inject
from bojojo import DB_DELETE_ERROR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, UNKNOWN_ERROR, AddError, DeleteError, GetError, UpdateError
from bojojo.adapters.db_response import DbResponse
from bojojo.adapters.service_result import ServiceResult
from bojojo.adapters.tst import tsts
from bojojo.base_service import Service
from bojojo.models.Completed_Run import CompletedRun
from bojojo.repositories.JobBoard_Repo import JobBoardRepository
from bojojo.services import ApplicationService, CompletedRunService, JobBoardService, JobTitleService, ResumeService, ScheduledRunService
from sqlalchemy.orm import Session

from bojojo.utils.dict_mapper import object_to_dict, proxy_to_dict
from bojojo.utils.service_injector import create_service
class DbHandler:

    appService = inject.attr(ApplicationService)
    completedRunService = inject.attr(CompletedRunService)
    jobBoardService = inject.attr(JobBoardService)
    # jobTitleService = inject.attr(JobTitleService)
    resumeService = inject.attr(ResumeService)
    scheduledRunService = inject.attr(ScheduledRunService)
    jobBoardRepo = inject.attr(JobBoardRepository)

    def __init__(
            self, 
            db_path: Path,
            appServ: Service,
            compServ: Service,
            jobBoardServ: Service,
            jobTitleServ: Service,
            resumeServ: Service,
            schedServ: Service
        ) -> None:
        self.__db_path = db_path
        self.appService = appServ
        self.completedRunService = compServ
        self.jobBoardService = jobBoardServ
        self.jobTitleService = jobTitleServ
        self.resumeService = resumeServ
        self.scheduledRunService = schedServ

    
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
        

    def read_application(self, name: str) -> DbResponse:
        try:
            app = self.appService.get_application(name)
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
            return ServiceResult(jobBoard, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def read_jobBoard_by_name(self, jname:str) -> DbResponse:
        try:
            jobBoard = self.jobBoardService.get_jobBoard_by_name(jname)
            return ServiceResult(jobBoard, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
        
    
    def read_all_jobBoards(self) -> DbResponse:
        try:
            jobBoards = self.jobBoardService.get_all_jobBoards()
            try:
                return ServiceResult(jobBoards, SUCCESS)
            except RuntimeError as e:
                return ServiceResult(str(e), UNKNOWN_ERROR)
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_job_board(self, sesh:Session, board_data:dict) -> DbResponse:
        try:
            board = self.jobBoardService.add_job_board(board_data)
            try:
                for rslt in board:
                    print(board)
                return board
                # return DbResponse([proxy_to_dict(board)], SUCCESS)
            except RuntimeError as e:
                return self.get_json_err(str(e))
        except AddError as e:
            print(e.message)
            return self.get_db_err(DB_WRITE_ERROR, e.message)
    

    def modify_job_board(self, id:int, board_data:dict) -> DbResponse:
        try:
            board = self.jobBoardService.update_job_board(id, board_data)
            try:
                return Service(board, SUCCESS)
            except Exception as e:
                return ServiceResult(str(e), UNKNOWN_ERROR)
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
    

    def read_job_title(self, id:int) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.get_job_title(id)
            return ServiceResult(jtitle, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def read_job_title_byName(self, title:str) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.get_job_title_by_name(title)
            return ServiceResult(jtitle, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_all_jobTitles(self) -> ServiceResult:
        try:
            jtitles = self.jobTitleService.get_all_jobTitles()
            return ServiceResult(jtitles, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def write_job_title(self, job_data:dict) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.add_job_title(job_data)
            return ServiceResult(jtitle, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
    
    
    def modify_job_title(self, id:int, job_data:dict) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.update_job_title(id, job_data)
            return ServiceResult(jtitle, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def modify_jobTitle_byName(self, name:str, job_data:dict) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.update_jobTitle_byName(name, job_data)
            return ServiceResult(jtitle, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def remove_job_title(self, id:int) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.delete_job_title(id)
            return ServiceResult(jtitle, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_jobTitle_byName(self, name:str) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.delete_jobTitle_byName(name)
            return ServiceResult(jtitle, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_all_jobTitles(self) -> ServiceResult:
        try:
            jtitle = self.jobTitleService.delete_all_jobTitles()
            return ServiceResult(jtitle, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)

        
    def read_resume(self, id:int) -> DbResponse:
        try:
            resume = self.resumeService.get_resume(id)
            try:
                return ServiceResult(resume, SUCCESS)
            except RuntimeError as e:
                return ServiceResult(str(e), UNKNOWN_ERROR)
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def read_all_resumes(self) -> DbResponse:
        try:
            resumes = self.resumeService.get_all_resumes()
            try:
                return ServiceResult(resumes, SUCCESS)
            except RuntimeError as e:
                return ServiceResult(str(e), UNKNOWN_ERROR)
        except GetError:
            return self.get_db_err(DB_READ_ERROR)
    

    def write_resume(self, resume_data:dict) -> DbResponse:
        try:
            resume = self.resumeService.add_resume(resume_data)
            try:
                return resume
            except:
                return self.get_json_err(str(e))
        except AddError as e:
            return self.get_db_err(DB_WRITE_ERROR, e.message)
    
    
    def modify_resume(self, name:str, resume_data:dict) -> DbResponse:
        try:
            resume = self.resumeService.update_resume(name, resume_data)
            try:
                return DbResponse(self.get_response(resume), SUCCESS)
            except:
                return self.get_json_err()
        except UpdateError:
            return self.get_db_err(DB_UPDATE_ERROR)
        
    
    def remove_resume(self, name:str) -> DbResponse:
        try:
            resume = self.resumeService.delete_resume(name)
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


    def get_response(self, obj) -> dict:
        return [obj.__dict__]
    
    
    def get_json_err(self, exmsg) -> DbResponse:
        return DbResponse([], JSON_ERROR, exmsg)
    

    def get_db_err(self, errType:int, excpMsg) -> DbResponse:
        return DbResponse([], errType, excpMsg)

    