from pathlib import Path
from typing import Any, Dict, List, NamedTuple

import inject
from sqlalchemy import create_engine
from bojojo import BOOLEAN_ERROR, CRON_WRITE_ERR, DB_READ_ERROR, DB_UPDATE_ERROR, DB_URL, DB_WRITE_ERROR, FILE_PATH_ERROR, SUCCESS, BooleanError, NoRecordError
from bojojo.adapters.current_item import CurrentItem
from bojojo.adapters.current_item_list import CurrentItemList
from bojojo.adapters.tst import tsts
from bojojo.base_model.base_model import init_db_models
from bojojo.factories.schedule_factory import ScheduleFactory
from bojojo.handlers import db_handler
import datetime

from bojojo.models.Cron_Schedule import CronSchedule
from bojojo.models.Scheduled_Run import ScheduledRun
from bojojo.providers.db_session_provider import session_provider
from bojojo.services.crontab_service import CronTabService
from bojojo.models.Cron_Schedule import CronSchedule
from bojojo.types import run_date
from bojojo.types.days import get_weekday
from bojojo.types.months import get_month_str
from bojojo.types.run_date import RunDate
from bojojo.types.schedule_types import ScheduleType
from bojojo.utils.dict_mapper import object_to_dict


class BojoController:


    dbHandler = inject.attr(db_handler.DbHandler)
    def __init__(self):
        self.sesh = session_provider()
    

    def createItem(self, reslt:Any) -> CurrentItem:
        return CurrentItem(reslt.entityList, reslt.excCode)
    

    def createItemList(self, reslt:Any) -> CurrentItemList:
        return CurrentItemList(reslt.entityList, reslt.excCode)
    

    def createErrorItem(self, errObj: Dict[str, Any], errCode:int) -> CurrentItem:
        return CurrentItem(item=errObj, excCode=errCode)
    

    def joinNameStr(self, name):
        return " ".join(name)
    
    
    def addJobBoard(self, name: List[str], url:str, hasEasyApply:int=0) -> CurrentItem:
        """Add a new job board to database to be used for job application submission"""
        nameTxt = self.joinNameStr(name)
        jboard = {
            "name": nameTxt,
            "url": url,
            "has_easy_apply": hasEasyApply
        }
        result = self.dbHandler.write_job_board(self.sesh, jboard)
        print(result)
        print(type(result))
        for r in result:
            print (r.name)
            print(r)

        return tsts(result, SUCCESS)
    

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
        result = self.dbHandler.read_job_board_byName(self.joinNameStr(name))
        return self.createItem(result)
    

    def modifyJobBoard(self, id:int, name: List[str], url:str, hasEasyApply:int=0) -> CurrentItem:
        """Update existing job board"""
        nameTxt = self.joinNameStr(name)
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
        nameTxt = self.joinNameStr(name)
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
        result = self.dbHandler.get_job_title_byName(self.joinNameStr(name))
        return self.createItem(result)
    

    def modifyJobTitle(self, id:int, name:List[str], experienceLvl:str, experienceYrs:int) -> CurrentItem:
        """Update an existing job title"""
        jname = self.joinNameStr(name)
        title = {
            "name": jname,
            "experience_level": experienceLvl,
            "experience_years": experienceYrs
        }
        result = self.dbHandler.modify_job_title(id, title)
        return self.createItem(result)
    

    def modifyJobTitleByName(self, name:List[str], experienceLvl:str, experienceYrs:int) -> CurrentItem:
        """Update an existing job title"""
        jname = self.joinNameStr(name)
        title = {
            "name": jname,
            "experience_level": experienceLvl,
            "experience_years": experienceYrs
        }
        result = self.dbHandler.modify_jobTitle_byName(title)
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
        result = self.dbHandler.read_resume_byName(self.joinNameStr(name))
        return self.createItem(result)
    

    def getAllResumes(self) -> CurrentItem:
        """Get all saved resumes"""
        results = self.dbHandler.get_all_resumes()
        return self.createItemList(results)
    

    def addResume(self, name:List[str], jobTitleId:int, filePath:str) -> CurrentItem:
        """Add resume to be used for a specific job title"""
        rname = self.joinNameStr(name)
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
    

    def modifyResume(self, name:List[str], jobTitleId:int, filePath: str) -> CurrentItem:
        """Update existing resume"""
        rname = self.joinNameStr(name)
        file_path = Path(filePath)
        resume = {
            "name": rname,
            "job_title_id": jobTitleId,
            "file_path": filePath
        }
        if not file_path.exists():
            return self.createErrorItem(resume, FILE_PATH_ERROR)
        result = self.dbHandler.modify_resume(name, resume)
        return self.createItem(result)
    

    def removeResume(self, name:str) -> CurrentItem:
        """Delete existing resume"""
        result = self.dbHandler.remove_resume(name)
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
        result = self.dbHandler.read_scheduled_run_byName(self.joinNameStr(name))
        return self.createItem(result)
    

    def addScheduleRun(self, name:List[str], jobTitleId:int, jobBoardId:int, onlyEasyApply:int, runType:ScheduleType=None) -> CurrentItem:
        """Save a Scheduled Run then enable it with enable command to automatically apply for a job title on specific job board"""

        sname = self.joinNameStr(name)

        #TODO might be able to handle in cli module
        # if onlyEasyApply != 0 or onlyEasyApply != 1:
        #     return BooleanError(BOOLEAN_ERROR)
        
        scheduledRun = {
            "name": sname,
            "job_title_id": jobTitleId,
            "job_board_id": jobBoardId,
            "run_type": runType.value,
            "creation_date": datetime.datetime.now(),
            "easy_apply_only": onlyEasyApply
        }

        dbresult = self.dbHandler.add_scheduled_run(scheduledRun)
        return self.createItem(dbresult)
    

    # TODO create schedule run method to add a scheduleRun that runs every so many hrs and mins
    def enableScheduledRun(self, name:List[str], run_date:RunDate, durMin:float, numSubmisn:int, repeat:bool) -> CurrentItem:
        """Enable an exsisting Scheduled Run by adding a schedule to automatically apply for a job title on job board"""

        sname = self.joinNameStr(name)
        run = self.dbHandler.read_schedule_run_byName(sname)

        if not run:
            return NoRecordError('schedule run', sname)
        
        run.run_day = run_date.day_of_month
        run.month = get_month_str(run_date.month)
        run.run_dayOf_week = get_weekday(run_date.day_of_week)
        run.run_time = f"{run_date.hour}:{run_date.minute}"
        run.durration_minutes = durMin
        run.number_of_submissions = numSubmisn
        run.recurring = 1 if repeat else 0
        run.every_hour = run_date.everyHour
        run.every_minute = run_date.everyMin
        dbresult = self.handler.update_scheduled_run(sname, object_to_dict(run))

        if not dbresult.excCode == SUCCESS:
            return self.createItem(dbresult)
        sched = self.get_schedule_dict(
            run.name,
            run.run_day,
            run.run_dayOf_week,
            run_date.hour,
            run_date.month,
            run_date.minute,
            run_date.everyHour,
            run_date.everyMin,
            durMin,
            numSubmisn
        )
        schedule = ScheduleFactory.getSchedule('other', **sched)
        #TODO applier bot will have to fetch jobTitle and jobBoard from db
        cron_scheduler = self.get_cron_service(schedule, run, self.dbHandler.get_path())

        #TODO make sure this works need to double check that crontab lib actually makes cronjobs and
        # if there is anything else that needs to be done when this is ran like permissions etc..
        #NOTE Read about CronTab lib
        
        # crontab areas on linux = /var/spool/cron or /var/spool/cron/crontabs/ on mac /var/cron/tabs/
        try:
            cron_scheduler.configureJobSchedule()
        except Exception as e:
            return self.createErrorItem({"EXC": e._message}, CRON_WRITE_ERR)
        #Keep db result
        return self.createItem(dbresult)
    

    def enableDailyScheduledRun(self, name:List[str], run_date:RunDate, durrMin:int, numbSubmissions:int) -> CurrentItem:
        sname = self.joinNameStr(name)
        run = self.dbHandler.read_scheduledRun_byName(sname)

        if not run:
            return NoRecordError('scheduled run', sname)
        run.run_day = run_date.day_of_month
        run.month = run_date.month
        run.run_dayOf_week = get_weekday(run_date.day_of_week)
        run.run_time = f"{run_date.hour}:{run_date.minute}"
        run.durration_minutes = durrMin
        run.number_of_submissions = numbSubmissions
        run.recurring = 1
        run.every_hour = run_date.everyHour
        run.every_minute = run_date.everyMin
        rslt, exCode = self.dbHandler.update_scheduled_run(sname, object_to_dict(run))
        if exCode != SUCCESS:
            return self.createErrorItem({}, DB_UPDATE_ERROR)
        
        sched = self.get_schedule_dict(
            run.name, 
            run.run_day,
            run.run_dayOf_week,
            run_date.hour,
            run_date.month,
            run_date.minute,
            run_date.everyHour,
            run_date.everyMin,
            durrMin,
            numbSubmissions
        )
        dailySchedule = ScheduleFactory.getSchedule('daily', **sched)
        cron_scheduler = self.get_cron_service(dailySchedule, run, self.dbHandler.get_path())

        try:
            cron_scheduler.configureJobSchedule()
        except Exception as e:
            return self.createErrorItem({"EXC": e._message}, CRON_WRITE_ERR)
        return self.createItem(rslt)
    

    def enableWeeklyScheduledRun(self, name:List[str], run_date:RunDate, durrMin:int, numbSubmissions:int) -> CurrentItem:
        sname = self.joinNameStr(name)
        run = self.dbHandler.read_scheduledRun_byName(sname)
        if not run:
            return NoRecordError('scheduled run', sname)
        run.run_day = run_date.day_of_month
        run.month = run_date.month
        run.run_dayOf_week = get_weekday(run_date.day_of_week)
        run.run_time = f"{run_date.hour}:{run_date.minute}"
        run.durration_minutes = durrMin
        run.number_of_submissions = numbSubmissions
        run.recourring = 1
        run.every_hour = run_date.everyHour
        run.every_minute = run_date.everyMin
        rslt, exCode = self.dbHandler.update_scheduled_run(sname, object_to_dict(run))

        if exCode != SUCCESS:
            return self.createErrorItem({}, DB_UPDATE_ERROR)
        
        sched = self.get_schedule_dict(
            run.name,
            run.run_day,
            run.run_dayOf_week,
            run_date.hour,
            run_date.month,
            run_date.minute,
            run_date.everyHour,
            run_date.everyMin,
            durrMin,
            numbSubmissions
        )
        weeklySchedule = ScheduleFactory.getSchedule('weekly', **sched)
        cron_scheduler = self.get_cron_service(weeklySchedule, run, self.dbHandler.get_path())

        try:
            cron_scheduler.configureJobSchedule()
        except Exception as e:
            return self.createErrorItem({"EXC": e._message}, CRON_WRITE_ERR)
        return self.createItem(rslt)

    
    def removeScheduledRun_byName(self, name:List[str]) -> CurrentItem:
        """Delete scheduled run from crontab and db by name"""
        sname = self.joinNameStr(name)
        runRslt = self.dbHandler.remove_scheduledRun_byName(sname)
        if not runRslt:
            return self.createErrorItem(runRslt.entityList, runRslt.excCode)
        requestRslt = CronTabService.removeScheduledJob()
        return CurrentItem(None, requestRslt)
    

    def removeAllScheduledRuns(self):
        runDbRslt = self.dbHandler.remove_all_scheduledRuns()
        if runDbRslt.excCode != SUCCESS:
            return self.createErrorItem({}, runDbRslt.excCode)
        cronRslt = CronTabService.removeAllScheduledJobs()
        if not cronRslt == SUCCESS:
            return [{}, cronRslt]
        return self.createItem(runDbRslt)
    

    def getCompletedRun(self, id:int) -> CurrentItem:
        crun = self.dbHandler.read_completed_run(id)
        return self.createItem(crun)
    

    def getAllCompletedRuns(self) -> CurrentItemList:
        cruns = self.dbHandler.read_all_completedRuns()
        return self.createItemList(cruns)


    def addCompletedRun(self, excDate:str, start:str, finish:str, apps_finished:int, failed_sumbissions:int, run_id:int) -> CurrentItem:
        crun = {
            "execution_date": excDate,
            "start": start,
            "finish": finish,
            "applications_finished": apps_finished,
            "failed_submissions": failed_sumbissions,
            "run_id": run_id
        }
        dbResult = self.dbHandler.write_completed_run(crun)
        return self.createItem(dbResult)
    
    
    def removeCompletedRun(self, id:int) -> CurrentItem:
        dbRslt = self.dbHandler.remove_completed_run(id)
        return self.createItem(dbRslt)


    def removeAllCompletedRuns(self) -> CurrentItemList:
        dbRslt = self.dbHandler.remove_all_completedRuns()
        return self.createItemList(dbRslt)
    

    def getApplication(self, name:str) -> CurrentItem:
        dbRslt = self.dbHandler.read_application(name)
        return self.createItem(dbRslt)
    

    def getAllApplications(self) -> CurrentItemList:
        dbRslt = self.dbHandler.read_all_applications()
        return self.createItemList(dbRslt)
    

    def deleteApplication(self, id:int) -> CurrentItem:
        dbRslt = self.dbHandler.delete_application(id)
        return self.createItem(dbRslt)
    
    
    def deleteAllApplications(self) -> CurrentItemList:
        dbRslt = self.dbHandler.delete_all_applications()
        return self.createItemList(dbRslt)
    

    def get_cron_service(schedule:CronSchedule, run:ScheduledRun, dbpath:str):
        return CronTabService.getScheduler(
            schedule,
            [run.job_title_id, run.job_board_id, dbpath]
        )        
    
    
    def get_schedule_dict(name, day, dayWeek, hr, mn, mnth, eHr, eMin, dMin, nSubs) -> Dict[str, Any]:
        return {
            "scheduleName": name,
            "day": day,
            "dayOfWeek": dayWeek,
            "hour": hr,
            "month": mnth,
            "minute": mn,
            "everyHour": eHr,
            "everyMinute": eMin,
            "durr": dMin,
            "numberSubmissions": nSubs            
        }
    
