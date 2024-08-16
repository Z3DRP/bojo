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

    # appService = inject.attr(ApplicationService)
    # completedRunService = inject.attr(CompletedRunService)
    # jobBoardService = inject.attr(JobBoardService)
    # # jobTitleService = inject.attr(JobTitleService)
    # resumeService = inject.attr(ResumeService)
    # scheduledRunService = inject.attr(ScheduledRunService)
    # jobBoardRepo = inject.attr(JobBoardRepository)

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

    
    def read_all_applications(self) -> ServiceResult:
        try:
            apps = self.appService.get_all_applications()
            return ServiceResult(apps, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        

    def read_application(self, id: int) -> ServiceResult:
        try:
            app = self.appService.get_application(id)
            return ServiceResult(app, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_applications_byname(self, name:str) -> ServiceResult:
        try:
            app = self.appService.get_application_byName(name)
            return ServiceResult(app, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        

    def write_applications(self, app_data:dict) -> ServiceResult:
        try:
            app = self.appService.add_application(app_data)
            return ServiceResult(app, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def modify_application(self, app_data:dict) -> ServiceResult:
        try:
            app = self.appService.update_application(app_data)
            return ServiceResult(app, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def remove_application(self, id:int) -> ServiceResult:
        try:
            app = self.appService.delete_application(id)
            return ServiceResult(app, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_all_applications(self) -> ServiceResult:
        try:
            app = self.appService.delete_all_applications()
            return ServiceResult(app, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def read_completed_run(self, id:int) -> ServiceResult:
        try:
            run = self.completedRunService.get_completed_run()
            return ServiceResult(run, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_all_completedRuns(self) -> ServiceResult:
        try:
            runs = self.completedRunService.get_all_completedRuns()
            return ServiceResult(runs, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def write_completed_run(self, run_data:dict) -> ServiceResult:
        try:
            run = self.completedRunService.add_completed_run(run_data)
            return ServiceResult(run, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
    

    def modify_completed_run(self, id:int, run_data:dict) -> ServiceResult:
        try:
            run = self.completedRunService.update_completed_run(id, run_data)
            return ServiceResult(run, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def remove_completed_run(self, id:int) -> ServiceResult:
        try:
            run = self.completedRunService.delete_completed_run(id)
            return ServiceResult(run, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_all_completeRuns(self) -> ServiceResult:
        try:
            run = self.completedRunService.delete_all_completedRuns()
            return ServiceResult(run, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
    

    def read_job_board(self, id:int) -> ServiceResult:
        try:
            jobBoard = self.jobBoardService.get_job_board(id)
            return ServiceResult(jobBoard, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def read_jobBoard_by_name(self, jname:str) -> ServiceResult:
        try:
            jobBoard = self.jobBoardService.get_jobBoard_by_name(jname)
            return ServiceResult(jobBoard, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
        
    
    def read_all_jobBoards(self) -> ServiceResult:
        try:
            jobBoards = self.jobBoardService.get_all_jobBoards()
            return ServiceResult(jobBoards, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def write_job_board(self, sesh:Session, board_data:dict) -> ServiceResult:
        try:
            board = self.jobBoardService.add_job_board(board_data)
            return ServiceResult(board, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
    

    def modify_job_board(self, id:int, board_data:dict) -> ServiceResult:
        try:
            board = self.jobBoardService.update_job_board(id, board_data)
            return ServiceResult(board, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def modify_jobboard_byName(self, name:str, board:dict) -> ServiceResult:
        try:
            board = self.jobBoardService.update_jobboard_byName(name, board)
            return ServiceResult(board, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
    

    def remove_job_board(self, id:int) -> ServiceResult:
        try:
            board = self.jobBoardService.delete_job_board(id)
            return ServiceResult(board, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_all_jobBoard(self) -> ServiceResult:
        try:
            board = self.jobBoardService.delete_all_jobBoards()
            return ServiceResult(board, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
    

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

        
    def read_resume(self, id:int) -> ServiceResult:
        try:
            resume = self.resumeService.get_resume(id)
            return ServiceResult(resume, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_all_resumes(self) -> ServiceResult:
        try:
            resumes = self.resumeService.get_all_resumes()
            return ServiceResult(resumes, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def write_resume(self, resume_data:dict) -> ServiceResult:
        try:
            resume = self.resumeService.add_resume(resume_data)
            return ServiceResult(resume, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
    
    
    def modify_resume(self, name:str, resume_data:dict) -> ServiceResult:
        try:
            resume = self.resumeService.update_resume(name, resume_data)
            return ServiceResult(resume, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
        
    
    def remove_resume(self, name:str) -> ServiceResult:
        try:
            resume = self.resumeService.delete_resume(name)
            return ServiceResult(resume, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_all_resumes(self) -> ServiceResult:
        try:
            resume = self.resumeService.delete_all_resumes()
            return ServiceResult(resume, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
            

    def read_scheduled_run(self, id:int) -> ServiceResult:
        try:
            run = self.scheduledRunService.get_scheduled_run(id)
            return ServiceResult(run, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_all_scheduledRuns(self) -> ServiceResult:
        try:
            runs = self.scheduledRunService.get_all_scheduledRuns()
            return ServiceResult(runs, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        
    
    def read_scheduledRuns_byType(self, type) -> ServiceResult:
        try:
            run = self.scheduledRunService.get_scheduledRun_byType(type)
            return ServiceResult(run, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
    

    def read_scheduled_run_byName(self, name:str) -> ServiceResult:
        try:
            run = self.scheduledRunService.get_scheduledRunByName(name)
            return ServiceResult(run, SUCCESS)
        except GetError as e:
            return ServiceResult(str(e), DB_READ_ERROR)
        

    def write_scheduled_run(self, run_data:dict) -> ServiceResult:
        try:
            run = self.scheduledRunService.add_scheduled_run(run_data)
            return ServiceResult(run, SUCCESS)
        except AddError as e:
            return ServiceResult(str(e), DB_WRITE_ERROR)
    

    def modify_scheduled_run(self, id:int, run_data:dict) -> ServiceResult:
        try:
            run = self.scheduledRunService.update_scheduled_run(id, run_data)
            return ServiceResult(run, SUCCESS)
        except UpdateError as e:
            return ServiceResult(str(e), DB_UPDATE_ERROR)
    

    def remove_scheduled_run(self, id:int) -> ServiceResult:
        try:
            run = self.scheduledRunService.delete_scheduled_run(id)
            return ServiceResult(run, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    
    def remove_scheduledRun_byName(self, name:str) -> ServiceResult:
        try:
            run = self.scheduledRunService.delete_scheduledRun_byName(name)
            return ServiceResult(run, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
            
    
    def remove_all_scheduledRuns(self) -> ServiceResult:
        try:
            run = self.scheduledRunService.delete_all_scheduledRuns()
            return ServiceResult(run, SUCCESS)
        except DeleteError as e:
            return ServiceResult(str(e), DB_DELETE_ERROR)
        
    