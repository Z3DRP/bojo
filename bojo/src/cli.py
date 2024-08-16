"""
This module provides the Bojo CLI
# bojo/cli.py
"""
from datetime import datetime, time
from pathlib import Path
from typing import List, Optional
from typing_extensions import Annotated
from sqlalchemy import create_engine
import typer
from bojojo import CONFIG_FILE_PATH, DB_URL, DEFAULT_DB_FILE_PATH, ERRORS, SUCCESS, __app_name__, __version__, db_path
from bojojo.base_model.base_model import init_db_models
from bojojo.controllers.bojo_controller import BojoController
from bojojo.services.crontab_service import CronTabService
from bojojo.src import config, db_config
from bojojo.repositories import db_init
from bojojo.inject_config import base_config
from rich.console import Console

from bojojo.types.days import WeekDays, get_weekday_int
from bojojo.types.experience_types import ExperienceType
from bojojo.types.months import Months, get_month_str
from bojojo.types.run_date import RunDate
from bojojo.types.schedule_types import ScheduleType
from bojojo.utils.cli_tables import get_multirow_table, get_singlerow_table
from bojojo.utils.dbhandler_injector import inject_handler
from bojojo.utils.dict_mapper import object_to_dict, stringify_dict


app = typer.Typer()

#TODO remove abilities to add alternate db path
@app.command()
def init() -> None:
    """Initialize Bojo database and create tables"""
    db_path_url = db_path()
    app_init_err = config.init_app(db_path_url)
    if app_init_err:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_err]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_err = db_init.initialize_db(Path(db_path_url))
    if db_init_err:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_err]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        try:
            engine = create_engine(DB_URL)
            init_db_models(engine)
        except Exception as e:
            typer.secho(
                f'Failed to initialize ORM model from SQL tables:: {e}',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        typer.secho(f"Bojo database created successfully at {db_path_url}", fg=typer.colors.GREEN)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

def get_controller() -> BojoController:
    if DEFAULT_DB_FILE_PATH.exists():
        return BojoController(inject_handler())
    else:
        typer.secho(
            'Database not found. Please, run "bojojo init"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


def print_table(table) -> None:
    console = Console()
    console.print(table)


@app.command()
def get_job_boards(
    name: Annotated[List[str], typer.Option("--name", "-n", help="Name of job board to retrieve")] = None,
    jid: Annotated[int, typer.Option("--id", "-i", help="Id of job board to get")] = None,
    all: Annotated[bool, typer.Option(default=..., is_flag=True, help="Flag to retrieve all saved job boards")] = False
) -> None:
    bcontroller = get_controller()
    jboard = None
    exCode = None
    jtable = None
    if all:
        jboard, exCode = bcontroller.getAllJobBoards()
    else:
        if name and jid or not name and not jid:
            typer.secho(
                f'Error, please enter only a job board name, id, or use the --all flag',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        elif name:
            jboard, exCode = bcontroller.getJobBoardByName(name)
        elif jid:
            jboard, exCode = bcontroller.getJobBoard(jid)
    if exCode != SUCCESS:
        typer.secho(
            f"Reading job board(s) failed with {ERRORS[exCode]}",
            fg=typer.colors.RED
        )
    else:
        typer.secho(
            "---Job Board Results",
            fg=typer.colors.GREEN,
            bold=True
        )
        table = get_multirow_table(jboard) if all or name else get_singlerow_table(**stringify_dict(jboard))
        print_table(table)
        

#TODO note unchange the changes made to ADD JOB BOARD METHOD depenency injection is working with the changes made to provider recently and adding the 
# create all to models.... might have to add the create all method in the commands maybe not though

#... is default for required
@app.command()
def add_job_board(
    name: Annotated[List[str], typer.Argument(..., help="Enter name of a job board to apply for jobs")],
    url: Annotated[str, typer.Argument(..., help="Enter the url for the job board")],
    easy_apply: Annotated[bool, typer.Option("--easy", "-e", help="Indicates the job board has a easy apply feature")] = False
) -> None:
    """Add a new job board that can be used to apply for jobs"""
    bcontroller = get_controller()
    jboard, exCode = bcontroller.addJobBoard(name, url, easy_apply)
    if exCode != SUCCESS:
        typer.secho(
            f'Adding job board failed with "{ERRORS[jboard.excCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"job-board: {jboard.item[0].name} was successfully added",
            fg=typer.colors.GREEN
        )
        jbtable = get_singlerow_table(**jboard)
        print_table(jbtable)


@app.command()
def update_job_board(
    name: Annotated[List[str], typer.Option(["--name", "-n"], help="Name of job board to update")],
    id: Annotated[int, typer.Option(["--id", "-i"], help="Id of job board to update")],
    url: Annotated[str, typer.Option(["--url", "-u"], help="Url for job board")],
    has_easy_apply: Annotated[Optional[bool], typer.Option(["--easy", "-e"], help="Indicates if the job board has a easy apply feature")]
) -> None:
    """Update a existing job board that is being used for job search"""
    bcontroller = get_controller()
    jobBoard = None
    exCode = None
    uptd_identifier = None
    if id:
        uptd_identifier = id
        jb = bcontroller.modifyJobBoard(id, name, url, has_easy_apply)
    elif name and not id:
        uptd_identifier = name
        jb = bcontroller.modifyJobBoardByName(name, url, has_easy_apply)
    else:
        typer.secho(
            "Error, please only specify a job board name or job board id",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if exCode != SUCCESS:
        typer.secho(
            f'Updating job board {uptd_identifier} failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'Job board: {uptd_identifier} was updated successfully',
            fg=typer.colors.GREEN
        )
        table = get_singlerow_table(
            **stringify_dict(jobBoard)
        )
        print_table(table)


@app.command()
def add_resume(
        name: Annotated[List[str], typer.Argument(..., help="Enter a name to help identify saved resumes")],
        job_id: Annotated[int, typer.Argument(..., help="Job id will link a resume to a specific job")],
        file_path: Annotated[str, typer.Argument(..., help="The file path where the resume can be found")]
) -> None:
    """Add a resume to be used for a specific job"""
    bcontroller = get_controller()
    resume, excCode = bcontroller.addResume(name, job_id, file_path)
    if excCode != SUCCESS:
        typer.secho(
            f'Adding resume failed with "{ERRORS[excCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Resume: {resume['name']} was successfully added",
            fg=typer.colors.GREEN
        )
        rtable = get_singlerow_table(
            **stringify_dict(resume)
        )
        print_table(rtable)
    

#TODO update resume to update based off name not id
@app.command()
def update_resume(
    name: Annotated[List[str], typer.Option(["--name", '-n'], help="Update resume name")],
    job_id: Annotated[int, typer.Option(["--job-id", "-jid"], help="Update job id to use resume with a different job")] = None,
    job_name: Annotated[List[str], typer.Option(..., help="Name of the job title for resume")] = None,
    file_path: Annotated[str, typer.Option(["--file-path", '-fp'], help="Update resume to point to a different file location")] = None
) -> None:
    """Update a saved resume"""
    bcontroller = get_controller()
    uptdResume = None
    exCode = None
    if not Path(file_path).exists():
        typer.secho(
            f'{file_path} is not a valid path please enter a path that exists',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        job = None
        if job_id:
            job, excode= bcontroller.getJobTitle(job_id)
        elif not job_id and job_name:
            job, excode = bcontroller.getJobTitleByName(job_name)
        if not job:
            typer.secho(
                f'A job title with id: {job_id} does not exist please create job title or enter a valid job id or name',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            uptdResume, exCode = bcontroller.modifyResume(name, job.id, file_path)
            if exCode != SUCCESS:
                typer.secho(
                    f'Updating resume failed with "{ERRORS[exCode]}"',
                    fg=typer.colors.RED
                )
                raise typer.Exit(1)
            else:
                typer.secho(
                    f'Resume: {name} was updated successfully',
                    fg=typer.colors.GREEN
                )
                table = get_singlerow_table(
                    **stringify_dict(uptdResume)
                )
                print_table(table)


@app.command()
def remove_resume(
    name: Annotated[List[str], typer.Option(["--name", "-n"], help="Name of resume to delete")],
    all: Annotated[bool, typer.Option(["--all", "-a"], help="Delete all saved resumes")]
) -> None:
    """Delete a resume or all resumes"""
    bcontroller = get_controller()
    delResumeCount = None
    exCode = None
    if all:
        delResumeCount, exCode = bcontroller.removeAllResumes()
    else:
        delResumeCount, exCode = bcontroller.removeResume(name)
    if exCode != SUCCESS:
        typer.secho(
            f'Deleting resume(s) failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Resume(s) deleted successfully, Rows Effected: {delResumeCount}",
            fg=typer.colors.GREEN
        )


@app.command()
def get_job_title(
    name: Annotated[List[str], typer.Option(default=..., help="Name of job title to retrieve")] = None,
    id: Annotated[int, typer.Option(default=..., help="Id of job title to get")] = None,
    all: Annotated[bool, typer.Option(default=..., help="Used to get all job titles")] = False
) -> None:
    """Get and display saved job titles"""
    bcontroller = get_controller()
    jobTitle = None
    exCode = None
    if all:
        jobTitle, exCode = bcontroller.getAllJobTitles()
    else:
        if name and id:
            typer.secho(
                f"Error, please enter only a job title name, job title id, or use the --all flag",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        elif name:
            jobTitle, exCode = bcontroller.getJobTitleByName(name)
        else:
            jobTitle, exCode = bcontroller.getJobTitle(id)
    if exCode != SUCCESS:
        typer.secho(
            f"Reading job title(s) failed with {ERRORS[exCode]}",
            fg=typer.colors.RED
        )  
        raise typer.Exit(1)
    else:
        typer.secho(
            "--Job Title Results--",
            fg=typer.colors.GREEN,
            bold=True
        )   
        table = get_multirow_table(jobTitle) if all else get_singlerow_table(**stringify_dict(jobTitle))
        print_table(table)


#TODO note date times can be used on dt values from typer cli arg types
#TODO might have to update experience years in service cls
@app.command()
def add_job_title(
    name: Annotated[List[str], typer.Argument(..., help="Enter the name of a job title to apply for")],
    experience_years: Annotated[float, typer.Argument(..., help="The years of experience for job title, value will be used in job search")],
    experience_level: Annotated[ExperienceType, typer.Argument(..., help="Experience level for job title, exepted values 'junior, mid, and senior'", case_sensitive=False)]
) -> None:
    """Add a job title to apply for"""
    bcontroller = get_controller()
    jobtitle, exCode = bcontroller.addJobTitle(name, experience_level, experience_years)
    if exCode != SUCCESS:
        typer.secho(
            f'Adding job title failed with "{ERRORS[jobtitle.excCode]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Job title: {jobtitle.name} was successfully added",
            fg=typer.colors.GREEN
        )
        ttable = get_singlerow_table(
            **stringify_dict(jobtitle)
        )
        print_table(ttable)
        

@app.command()
def update_job_title(
    job_id: Annotated[int, typer.Option(default=..., help="Specifies the id of the job title to change")] = None,
    name: Annotated[List[str], typer.Option(default=..., help="Change the name of a saved job title")] = None,
    experience_years: Annotated[float, typer.Option(default=..., help="Update the years of experience for a job title")] = None,
    experience_level: Annotated[ExperienceType, typer.Option(default=..., help="Update the level of experience for a job title, expected values 'junior, mid, senior'", case_sensitive=False)] = None
) -> None:
    """Update a job title to apply for"""
    bcontroller = get_controller()
    updatedJob = None
    exCode = None
    if job_id:
        updatedJob, exCode = bcontroller.modifyJobTitle(job_id, name=name, experienceYrs=experience_years, experienceLvl=experience_level)
    elif name and not job_id:
        updatedJob, exCode = bcontroller.modifyJobTitleByName(name, experienceLvl=experience_level, experienceYrs=experience_years)
    else:
        typer.secho(
            "Error, please only specify a job title or job title id",
            fg=typer.colors.RED
        )
    if exCode != SUCCESS:
        typer.secho(
            f'Updating job title {name} failed with "{ERRORS[exCode]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Job title: {''.join(name)} was updated successfully",
            fg=typer.colors.GREEN
        )

        ttable = get_singlerow_table(
            **stringify_dict(updatedJob)
        )
        print_table(ttable)


#TODO need to add a delete by name method and update name of current delete method
@app.command()
def remove_job_title(
    name: Annotated[List[str], typer.Option(..., help="Specifies the name of a job title to delete")] = None,
    job_id: Annotated[int, typer.Option(..., help="Specifies the id of a job title to delete")] = None,
    all: Annotated[bool, typer.Option(..., help="Delete all saved job titles")] = None
) -> None:
    """Delete a job title using the name or id"""
    bcontroller = get_controller()
    deletedJobs = None
    exCode = None
    deleteByVal = None
    if all:
        deletedJobs, exCode = bcontroller.removeAllJobTitles()
    else:
        if name and not job_id:
            deletedJobs, exCode = bcontroller.removeJobTitleByName(name)
        elif job_id and not name:
            deleteByVal = name if name is not None else job_id
            deletedJobs, exCode = bcontroller.removeJobTitleById(job_id)
        else:
            typer.secho(
                "Error, please only specify a job title name or job title id",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
    if exCode != SUCCESS:
        typer.secho(
            f'Deleting job title {deleteByVal} failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        # dltcount = sum(chunk.rowcount for chunk in deletedJobs.partitions())
        typer.secho(
            f"Job title: {''.join(name)} was deleted successfully, Rows Effected {deletedJobs}",
            fg=typer.colors.GREEN
        )


#TODO
@app.command()
def getScheduledSearches(
    type: Annotated[ScheduleType, typer.Option(..., help="Type of scheduled search to find")] = None,
    id: Annotated[int, typer.Option(..., help="id of a scheduled search to find")] = None,
    name: Annotated[List[str], typer.Option(..., help="name of scheduled search to find")] = None,
    all: Annotated[bool, typer.Option(..., help="Flag to read all saved scheduled searches")] = False
) -> None: 
    """Get and display a saved scheduled job search by name or type"""
    bcontroller = get_controller()
    search = None
    exCode = None
    if all:
        search, exCode = bcontroller.getAllScheduledRuns()
    else:
        if type:
            search, exCode = bcontroller.getScheduledRunByType(type)
        if id:
            search, exCode = bcontroller.getScheduledRun(id)
        # TODO code by name method
        elif name:
            search, exCode = bcontroller.getScheduledRunByName(name)
    if exCode != SUCCESS:
        typer.secho(
            f'Reading scheduled searches failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            "--Scheduled Searches--",
            fg=typer.colors.GREEN,
            bold=True
        )
        table = get_multirow_table(search) if all else get_singlerow_table(**stringify_dict(search))
        print_table(table)

@app.command()
#needs name,jobTitleId,jobBoardId,runType,easyApplyOnly
def addScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="Specify a name to identify a scheduled search")],
    jobName: Annotated[List[str], typer.Arguement(..., help="Specify the job title name to apply for")],
    jobBoardName: Annotated[List[str], typer.Argument(..., help="Specify the job board name to use for search")],
    useEasyApplyOnly: Annotated[bool, typer.Option(..., help="Specifies if job search should only use the easy apply feature on the job board")] = False
) -> None:
    """Create a scheduled job search runs automatically on specified schedule using crontab, can be set to run once, daily, weekly, monthlly"""
    bcontroller = get_controller()
    jtid = None
    jbid = None
    exCode = None
    relation_ids = {}
    if jobName:
        jobTitle, ecode = bcontroller.getJobTitleByName(name)
        if not jobTitle:
            typer.secho(f"Command failed, no job title found with name '{jobName}', please enter valid job title name", fg=typer.colors.RED)
        else:
            relation_ids['jobtitleid'] = jobTitle.id
    if jobBoardName:
        jobBoard, ecode = bcontroller.getJobBoardByName("".join(jobBoardName))
        if not jobBoard:
            typer.secho(f"Command faild, no job board found with name '{jobBoardName}', please enter a valid job board name", fg=typer.colors.RED)
        else:
            relation_ids['jobboardid'] = jobBoard.id
    scheduledRun, exCode = bcontroller.addScheduleRun(
        name,
        jobTitleId=relation_ids['jobtitleid'],
        jobBoardId=relation_ids['jobboardid'],
        onlyEasyApply=useEasyApplyOnly
    )
    if exCode != SUCCESS:
        typer.secho(
            f'Creating schedule run failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Scheduled Run created successfully",
            fg=typer.colors.GREEN
        )
        stable = get_singlerow_table(
            **stringify_dict(scheduledRun)
        )
        print_table(stable)


@app.command()
#needs name,runDay,runDayOfWeek,runHr,runMin,durMin,numbSubmissions
# TODO if initial start is different than the day of week then use day of week instead of datetime day
def enableScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="Name of a previously created scheduled search")],
    runDateTime: Annotated[
        datetime, 
        typer.Option(
            ...,
            help="The date and time of the initial run", 
            formats=["%d/%m/ %H:%M", "%d-%m %H:%M"]
        )] = None,
    durrationMinutes: Annotated[int, typer.Option(..., help="Sets the the length of time in minutes the search runs")]=30,
    numberOfSubmissions: Annotated[int, typer.Option(..., help="Indicates the number of submissions the search should complete before exiting")]=None,
    everyHours: Annotated[int, typer.Option(..., help="Sets the scheduled search to run every x hours")]=None,
    everyMins: Annotated[int, typer.Option(..., help="Sets the scheduled search to run every x minutes")]=None,
    runType: Annotated[ScheduleType, typer.Option(..., help="Indicates the scheduled search run type, defaults to once")]=ScheduleType.ONCE

) -> None:
    """Enables previous scheduled searches to automatically run at a set date and time, certain days of weeks, certain days of the month, every x amount of hours, or every x amount of minutes"""
    bcontroller = get_controller()
    scheduledRun, exCode = bcontroller.getScheduledRun(name)
    if not scheduledRun:
        typer.secho(
            f'Enabled scheduled search failed with error "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    
    #TODO fix to use runDateTime and pull out days etc from that or use runTime and other
    run_data = None 
    run_date = RunDate(
        monthDay = runDateTime.day, 
        weekDay = WeekDays(runDateTime.weekday()), 
        month = Months(runDateTime.month), 
        hour = runDateTime.hour, 
        minute = runDateTime.minute, 
        everyHr = everyHours,
        everyMin = everyMins, 
        runType = runType
    )

    scheduledRun, exCode = bcontroller.enableScheduledRun(
        name, 
        run_date,
        durrationMinutes,
        numberOfSubmissions
    )

    if exCode != SUCCESS:
        typer.secho(
            f'Enable scheduled search failed with error "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    
    typer.secho(
        f'Scheduled search "{scheduledRun["name"]}" was enabled successfully, it will begin executing at "{datetime.isofrmat(runDateTime)}"',
        fg=typer.colors.GREEN
    )
    stable = get_singlerow_table(
        stringify_dict(**scheduledRun)
    )
    print_table(stable)
        

# for these next 3 commands pass in a date time and then a day of week or day of month have opt for every hour/mins
@app.command()
def enableDailyScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="The name of a previously saved scheduled search")],
    time: Annotated[
        datetime, 
        typer.Argument(
            ...,
            formats=["%H:%M", "%H %M"],
            help='Time the scheduled search should occur'
    )],
    everyHour: Annotated[int, typer.Option(..., help="Sets the scheduled search to run every x hours")],
    everyMin: Annotated[int, typer.Option(..., help="Sets the scheduled search to run every x minutes")],
    durrationMin: Annotated[int, typer.Option(..., help="Sets the durration of the search in minutes, defaults to 30")]=30,
    numberOfSubs: Annotated[int, typer.Option(..., help="Sets the number of submissions for search to complete before exiting")]=None
) -> None:
    """Enable a scheduled search to run daily at a specific time"""
    bcontroller = get_controller()
    scheduledRun, exCode = bcontroller.getScheduledRun(name)
    if not scheduledRun:
        typer.secho(
            f'Enable daily search failed, there is no previous scheduled run named "{" ".join(name)}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if exCode != SUCCESS:
        typer.secho(
            f'Enabled daily search failed with errors: "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    run_data = RunDate.create_daily(time.hour, time.minute, everyHour, everyMin, durrationMin)
    scheduledRun, exCode = bcontroller.enableDailyScheduledRun(name, run_data, durrationMin, numberOfSubs)
    if exCode != SUCCESS:
        typer.secho(
            f'Enabled daily search failed with errors: "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho(
        f'Daily search for "{name}" enabled successfully',
        fg=typer.colors.GREEN
    )
    stable = get_singlerow_table(
        stringify_dict(**scheduledRun)
    )
    print_table(stable)


@app.command()
def enableWeeklyScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="The name of a previously saved scheduled search")],
    time: Annotated[
        datetime,
        typer.Argument(
            ...,
            formats=["%H:%M", "%H %M"],
            help="Time the daily scheduled search should occur"
    )],
    weekday: Annotated[WeekDays, typer.Argument(..., help="The day of the week the scheduled search should run")],
    everyHour: Annotated[int, typer.Option(..., help="Sets the search to run every x hours")],
    everyMin: Annotated[int, typer.Option(..., help="Sets the search to run every x minutes")],
    durrationMin: Annotated[int, typer.Option(..., help="Sets the durration of the search in minutes, defatuls to 30")]=30,
    numberOfSubs: Annotated[int, typer.Option(..., help="Sets the number of submissions for search to complete before exiting")]=None
) -> None:
    """Enable a schedule search to run weekly on a specific day and time"""
    bcontroller = get_controller()
    scheduledRun, exCode = bcontroller.getScheduledRun(name)
    if not scheduledRun:
        typer.secho(
            f'Enable daily search failed, there is no previous scheduled run named "{" ".join(name)}"',
            fg=typer.colors.RED            
        )
        raise typer.Exit(1)
    if exCode != SUCCESS:
        typer.secho(
            f'Enabled daily search failed with errors: "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    run_data = RunDate.create_weekly(weekday, time.hour, time.minute, everyHour, everyMin, durrationMin)
    scheduledRun, exCode = bcontroller.enableWeeklyScheduledRun(name, run_data, durrationMin, numberOfSubs)        
    if exCode != SUCCESS:
        typer.secho(
            f'Enabled daily search failed with errors: "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)        
    typer.secho(
        f'Weekly search for "{name}" enabled successfully',
        fg=typer.colors.GREEN
    )
    stable = get_singlerow_table(
        stringify_dict(**scheduledRun)
    )
    print_table(stable)    


@app.command()
def enableMontlyScheduledSearch():
    """Enable a schedule search to run montly on a specific day and time"""
    typer.secho(
        "Enable monthly schedule not implemented yet",
        fg=typer.colors.YELLOW
    )
    pass


@app.command()
def getScheduleSearch(
    name: Annotated[List[str], typer.Option(None, help="Name of a Scheduled Search")] = None,
    run_type: Annotated[ScheduleType, typer.Option(None, help="Scheduled Search run type to look for")] = None,
    all: Annotated[bool, typer.Option(None, help="Flag to retrieve all Scheduled Searches")] = False
) -> None:
    """Get all Scheduled Searches"""
    bcontroller = get_controller()
    searches = None
    exCode = None
    if all:
        searches, exCode = bcontroller.getAllScheduledRuns()
    if name and not all:
        searches, exCode = bcontroller.getScheduledRunByName(name)
    elif run_type and not all:
        searches, exCode = bcontroller.getScheduledRunByType()
    else:
        typer.secho(
            f"Error, please enter a name, run type, or use the all flag",
            fg=typer.colors.RED
        )
        typer.Exit(1)
    for search in searches:
        search.setNext(CronTabService.getNext(search))
        search.setPrevious(CronTabService.getPrevious(search))
        search.setIsValid(CronTabService.isValid(search))
        search.setIsEnabled(CronTabService.isEnabled(search))
    #TODO create table with the values
    table = None
    if len(searches) == 0:
        typer.secho(
            f'No Schedule Search records found',
            fg=typer.colors.RED
        )
    elif len(searches) > 1:
        table = get_multirow_table(searches)
        print_table(table)
    else:
        table = get_singlerow_table(**stringify_dict(searches))
        print_table(table)
    
    



@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return


def convert_entity_list(entity_list):
    nw_list = []
    for entity in entity_list:
        nw_list.append(stringify_dict(entity))
    return nw_list
