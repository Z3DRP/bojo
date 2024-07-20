from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from bojojo import DB_READ_ERROR, DB_WRITE_ERROR
from bojojo.adapters.current_item import CurrentItem
from bojojo.adapters.current_item_list import CurrentItemList
from bojojo.handlers import db_handler
from injector import inject


class BojoController:
    
    @inject
    def __init__(self, dbHandler: db_handler):
        self.dbHandler = dbHandler

    
    def createItem(self, reslt:Any) -> CurrentItem:
        return CurrentItem(reslt.entityList, reslt.excCode)
    

    def createItemList(self, reslt:Any) -> CurrentItemList:
        return CurrentItemList(reslt.entityList, reslt.excCode)
    
    
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
    
    
    def getJobBoardByName(self, name:str) -> CurrentItem:
        """Return a specific job board by name"""
        result = self.dbHandler.read_job_board_byName(name)
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
    
    
    def getJobTitleByName(self, name:str) -> CurrentItem:
        """Get a specific job title by name"""
        result = self.dbHandler.get_job_title_byName(name)
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
    

    def getResume


