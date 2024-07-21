from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR, FILE_PATH_ERROR
from bojojo.adapters.current_item import CurrentItem
from bojojo.adapters.current_item_list import CurrentItemList
from bojojo.handlers import db_handler
from injector import inject
import datetime

from bojojo.services.scheduler_service import SchedulerService


class BojoController:
    
    @inject
    def __init__(self, dbHandler: db_handler):
        self.dbHandler = dbHandler

    
    def createItem(self, reslt:Any) -> CurrentItem:
        return CurrentItem(reslt.entityList, reslt.excCode)
    

    def createItemList(self, reslt:Any) -> CurrentItemList:
        return CurrentItemList(reslt.entityList, reslt.excCode)
    

    def createErrorItem(self, errObj: Dict[str, Any], errCode:int) -> CurrentItem:
        return CurrentItem(item=errObj, excCode=errCode)
    

    def getRoot(self) -> Path:
        pathlib.
    
    def addJobBoard(self, name: List[str], url:str, hasEasyApply:int=0) -> CurrentItem:
        """Add a new job board to database to be used for job application submission"""
        nameTxt = " ".join(name)
        jboard = {
            "name": nameTxt,
            "url": url,
            "has_easy_apply": hasEasyApply
        }
        result = self.dbHandler.write_job_board(jboard)
        return self.createItem(result)
    

    def getJobBoard(self, id:int) -> CurrentItem:
        """Return a specific job board by id"""
        result = self.dbHandler.read_job_board(id)
        return self.createItem(result)


    def getAllJobBoards(self) -> CurrentItemList:
        """Return all saved job boards"""
        result = self.dbHandler.read_all_jobBoards()
        return self.createItemList(result)
    
    
    def getJobBoardByName(self, name:List[str]) -> CurrentItem:
        """Return a specific job board by name"""
        result = self.dbHandler.read_job_board_byName(" ".join(name))
        return self.createItem(result)
    

    def modifyJobBoard(self, id:int, name: List[str], url:str, hasEasyApply:int=0) -> CurrentItem:
        """Update existing job board"""
        nameTxt = " ".join(name)
        jboard = {
            "name": nameTxt,
            "url": url,
            "has_easy_apply": hasEasyApply
        }
        result = self.dbHandler.modify_job_board(id, jboard)
        return self.createItem(result)
    

    def removeJobBoard(self, id:int) -> CurrentItem:
        """Delete existing job board"""
        result = self.dbHandler.remove_job_board(id)
        return self.createItem(result)
    

    def removeAllJobBoards(self) -> CurrentItem:
        """Delete all existing job boards"""
        result = self.dbHandler.remove_all_jobBoards()
        return self.createItem(result)


    def addJobTitle(self, name:List[str], experienceLvl:str, experienceYrs:int) -> CurrentItem:
        """Add job title to apply for"""
        nameTxt = " ".join(name)
        title = {
            "name": nameTxt,
            "experience_level": experienceLvl,
            "experience_years": experienceYrs
        }
        result = self.dbHandler.write_job_title(title)
        return self.createItem(result)
    

    def getJobTitle(self, id:int) -> CurrentItem:
        """Get a specific job title by id"""
        result = self.dbHandler.read_job_title(id)
        return self.createItem(result)
    

    def getAllJobTitles(self) -> CurrentItemList:
        """Get all job titles"""
        results = self.dbHandler.get_all_jobTitles()
        return self.createItemList(results)
    
    
    def getJobTitleByName(self, name:List[str]) -> CurrentItem:
        """Get a specific job title by name"""
        result = self.dbHandler.get_job_title_byName(" ".join(name))
        return self.createItem(result)
    

    def modifyJobTitle(self, id:int, name:List[str], experienceLvl:str, experienceYrs:int) -> CurrentItem:
        """Update an existing job title"""
        jname = " ".join(name)
        title = {
            "name": jname,
            "experience_level": experienceLvl,
            "experience_years": experienceYrs
        }
        result = self.dbHandler.modify_job_title(id, title)
        return self.createItem(result)


    def removeJobTitle(self, id:int) -> CurrentItem:
        """Delete a job title"""
        result = self.dbHandler.remove_job_title(id)
        return self.createItem(result)
    

    def removeAllJobTitles(self) -> CurrentItem:
        """Delete all job titles"""
        result = self.dbHandler.remove_all_jobTitles()
        return self.createItem(result)
    

    def getResume(self, id:int) -> CurrentItem:
        """Get a specific resume by id"""
        result = self.dbHandler.read_resume(id)
        return self.createItem(result)
    

    def getResume(self, name:List[str]) -> CurrentItem:
        """Get a specific resume by name"""
        result = self.dbHandler.read_resume_byName(" ".join(name))
        return self.createItem(result)
    

    def getAllResumes(self) -> CurrentItem:
        """Get all saved resumes"""
        results = self.dbHandler.get_all_resumes()
        return self.createItemList(results)
    

    def addResume(self, name:List[str], jobTitleId:int, filePath:str) -> CurrentItem:
        """Add resume to be used for a specific job title"""
        rname = " ".join(name)
        file_path = Path(filePath)
        resume = {
            "name": rname,
            "job_title_id": jobTitleId,
            "file_path": filePath
        }
        if not file_path.exists():
            return self.createErrorItem(resume, FILE_PATH_ERROR)
        result = self.dbHandler.write_resume(resume)
        return self.createItem(result)
    

    def modifyResume(self, id:int, name:List[str], jobTitleId:int, filePath: str) -> CurrentItem:
        """Update existing resume"""
        rname = " ".join(name)
        file_path = Path(filePath)
        resume = {
            "name": rname,
            "job_title_id": jobTitleId,
            "file_path": filePath
        }
        if not file_path.exists():
            return self.createErrorItem(resume, FILE_PATH_ERROR)
        result = self.dbHandler.modify_resume(id, resume)
        return self.createItem(result)
    

    def removeResume(self, id:int) -> CurrentItem:
        """Delete existing resume"""
        result = self.dbHandler.remove_resume(id)
        return self.createItem(result)
    

    def removeAllResumes(self) -> CurrentItem:
        """Delete all existing resumes"""
        result = self.dbHandler.remove_all_resumes()
        return self.createItem(result)
    

    def getScheduledRun(self, id:int) -> CurrentItem:
        """Get a specific scheduled run by id"""
        result = self.dbHandler.read_scheduled_run(id)
        return self.createItem(result)
    

    def getAllScheduledRuns(self) -> CurrentItemList:
        """Get all scheduled runs"""
        results = self.dbHandler.read_all_scheduledRuns()
        return self.createItemList(results)
    

    def getScheduledRun(self, name:List[str]) -> CurrentItem:
        """Get a specific scheduled run by name"""
        result = self.dbHandler.read_scheduled_run_byName(" ".join(name))
        return self.createItem(result)
    

    def addScheduledRun(self, name:List[str], jobTitleId:int, jobBoardId:int, runDay:str, runMonth:str, runDayOfWeek:str, runTime:str, runType:str, repeat:int, onlyEasyApply:int) -> CurrentItem:
        """Create Scheduled Run to automatically apply to job title on specific job board"""
        sname = " ".join(name)
        scheduledRun = {
            "name": sname,
            "job_title_id": jobBoardId,
            "job_board_id": jobBoardId,
            "run_date": f"{runDay}/{runMonth}",
            "run_type": runType,
            "run_dayOf_week": runDayOfWeek,
            "run_time": runTime,
            "creation_date": datetime.datetime.now(),
            "reocurring": repeat,
            "easy_apply_only": onlyEasyApply
        }
        #TODO make sure this works need to double check that crontab lib actually makes cronjobs and
        # if there is anything else that needs to be done when this is ran like permissions etc..
        #NOTE Read about CronTab lib

        #TODO create instance of cron_schedul cls then pass cron_schedul,  and script args(dbLoc, website, jobtitle) to scheduelrCls
        
        # crontab areas on linux = /var/spool/cron or /var/spool/cron/crontabs/ on mac /var/cron/tabs/
        isoDateTime = f"{rnDate[2]}-{month}-{day}"
        time = runTime.split(':')
        hr = time[0]
        minutes = time[1]
        schedule = datetime.datetime(rnDate[2], rnDate[1], rnDate[0], hr, minutes)
        cronJobScheduler = SchedulerService.getScheduler()
        cronJobScheduler.scheduleJob(schedule)

        #Keep db result
        dbresult = self.dbHandler.add_scheduled_run(scheduledRun)
        return self.createItem(dbresult)



