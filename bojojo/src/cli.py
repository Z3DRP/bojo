"""
This module provides the Bojo CLI
# bojo/cli.py
"""
from datetime import datetime
from pathlib import Path
from typing import Annotated, List, Optional
import typer
from bojojo import CONFIG_FILE_PATH, DEFAULT_DB_FILE_PATH, ERRORS, SUCCESS, __app_name__, __version__, db_path
from bojojo.controllers.bojo_controller import BojoController
from bojojo.src import config, db_config
from bojojo.repositories import db_init
from bojojo.inject_config import base_config
from rich.console import Console

from bojojo.types.days import WeekDays, get_weekday_int
from bojojo.types.months import Months, get_month_str
from bojojo.types.run_date import RunDate
from bojojo.types.schedule_types import ScheduleType
from bojojo.utils.cli_tables import get_multirow_table, get_singlerow_table


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
        typer.secho(f"Bojo database created successfully at {db_path_url}", fg=typer.colors.GREEN)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

def get_controller() -> BojoController:
    if DEFAULT_DB_FILE_PATH.exists():
        return BojoController()
    else:
        typer.secho(
            'Database not found. Please, run "bojojo init"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


def print_table(table) -> None:
    console = Console()
    console.print(table)


#... is default for required
@app.command()
def add_job_board(
    name: Annotated[List[str], typer.Argument(..., help="Enter name of a job board to apply for jobs")],
    url: Annotated[str, typer.Argument(..., help="Enter the url for the job board")],
    easy_apply: Annotated[bool, typer.Option("--easy", "-e", help="Indicates the job board has a easy apply feature")] = False
) -> None:
    """Add a new job board that can be used to apply for jobs"""
    bcontroller = get_controller()
    has_easy = 1 if easy_apply else 0
    jboard, excCode = bcontroller.addJobBoard(name, url, has_easy)
    if excCode != SUCCESS:
        typer.secho(
            f'Adding job board failed with "{ERRORS[excCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"job-board: {jboard['name']} was successfully added",
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
    has_easy = 1 if has_easy_apply else 0
    jobBoard = None
    exCode = None
    jid = None
    if name:
        jb = bcontroller.getJobBoardByName(''.join(name))
        if not jb.item:
            typer.secho(
                f'Update job board failed, no job board with name "{" ".join(name)}" exists, please enter a valid job board name or id',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        jid = jb['id']
    if id:
        jb = bcontroller.getJobBoard(id)
        if not jb.item:
            typer.secho(
                f'Update job board failed, no job board with id "{id}" exists, please enter a valid job board id or name',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
    if not name and not id:
        typer.secho(f"Command failed, please specify a job board name or id", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    jobBoard, exCode = bcontroller.modifyJobBoard(id=jid if name else id, name=name, url=url, hasEasyApply=has_easy)
    if exCode != SUCCESS:
        typer.secho(
            f"Update job board failed with {ERRORS[exCode]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        jtable = get_singlerow_table(**jtable)
        print_table(jtable)


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
        rtable = get_singlerow_table(**resume)
        print_table(rtable)
    

#TODO update resume to update based off name not id
@app.command()
def update_resume(
    name: Annotated[List[str], typer.Option(["--name", '-n'], help="Update resume name")],
    job_id: Annotated[int, typer.Option(["--job-id", "-jid"], help="Update job id to use resume with a different job")],
    file_path: Annotated[str, typer.Option(["--file-path", '-fp'], help="Update resume to point to a different file location")]
) -> None:
    """Update a saved resume"""
    bcontroller = get_controller()
    resume, excCode = bcontroller.modifyResume(name, job_id, file_path)
    if excCode != SUCCESS:
        typer.secho(
            f'Updating resume failed with "{ERRORS[excCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Resume: {resume['name']} was successfully added",
            fg=typer.colors.GREEN
        )
        rtable = get_singlerow_table(**resume)
        print_table(rtable)


@app.command()
def remove_resume(
    name: Annotated[List[str], typer.Option(["--name", "-n"], help="Name of resume to delete")],
    all: Annotated[bool, typer.Option(["--all", "-a"], help="Delete all saved resumes")]
) -> None:
    """Delete a resume or all resumes"""
    bcontroller = get_controller()
    resumes = None
    exCode = None
    if all:
        resumes, exCode = bcontroller.removeAllResumes()
    else:
        resumes, exCode = bcontroller.removeResume
    if exCode != SUCCESS:
        typer.secho(
            f'Deleting resume(s) failed with "{ERRORS[exCode]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Resume(s) deleted successfully",
            fg=typer.colors.GREEN
        )
        rtable = None
        if all:
            rtable = get_multirow_table(*resumes)
        else:
            rtable = get_singlerow_table(**resumes)
        print_table(rtable)


#TODO note date times can be used on dt values from typer cli arg types
#TODO might have to update experience years in service cls
@app.command()
def add_job_title(
    name: Annotated[List[str], typer.Argument(..., help="Enter the name of a job title to apply for")],
    experience_years: Annotated[float, typer.Argument(..., help="The years of experience for job title, value will be used in job search")],
    experience_level: Annotated[str, typer.Argument(..., help="Experience level for job title, exepted values 'junior, mid, and senior'")]
) -> None:
    """Add a job title to apply for"""
    bcontroller = get_controller()
    jobtitle, exCode = bcontroller.addJobBoard(name, experience_level, experience_years)
    if exCode != SUCCESS:
        typer.secho(
            f'Adding job title failed with "{ERRORS[exCode]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Job title: {jobtitle['name']} was successfully added",
            fg=typer.colors.GREEN
        )
        ttable = get_singlerow_table(**jobtitle)
        print_table(ttable)
        

@app.command()
def update_job_title(
    job_id: Annotated[int, typer.Option(["--jid", "-id"], help="Specifies the id of the job title to change")],
    name: Annotated[List[str], typer.Option(["--name", "-n"], help="Change the name of a saved job title")],
    experience_years: Annotated[float, typer.Option(["--xp-years", "-y"], help="Update the years of experience for a job title")],
    experience_level: Annotated[str, typer.Option(["--xp-level", "-l"], help="Update the level of experience for a job title, expected values 'junior, mid, senior'")]
) -> None:
    """Update a job title to apply for"""
    bcontroller = get_controller()
    updatedJob = None
    exCode = None
    if name and not job_id:
        updatedJob, exCode = bcontroller.modifyJobTitle(job_id, experienceYrs=experience_years, experienceLvl=experience_level)
    elif job_id and not name:
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
        ttable = get_singlerow_table(**updatedJob)
        print_table(ttable)


#TODO need to add a delete by name method and update name of current delete method
@app.command()
def remove_job_title(
    name: Annotated[List[str], typer.Option(["--name", "-n"], help="Specifies the name of a job title to delete")],
    job_id: Annotated[int, typer.Option(["--job-title-id", "-jti"], help="Specifies the id of a job title to delete")],
    all: Annotated[bool, typer.Option(["--all", "-a"], help="Delete all saved job titles")]
) -> None:
    """Delete a job title using the name or id"""
    bcontroller = get_controller()
    deletedJobs = None
    exCode = None
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
        typer.secho(
            f"Job title: {''.join(name)} was deleted successfully",
            fg=typer.colors.GREEN
        )
        jTable = None
        if all:
            jTable = get_multirow_table(*deletedJobs)
        else:
            jTable = get_singlerow_table(**deletedJobs)
        print_table(jTable)


#TODO
@app.command()
def getScheduledSearches() -> None:
    bcontroller = get_controller()
    runs = bcontroller.readScheduledRuns()


@app.command()
#needs name,jobTitleId,jobBoardId,runType,easyApplyOnly
def addScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="Specify a name to identify a scheduled search")],
    jobTitleId: Annotated[int, typer.Option(["--title-id", "-jtid"], help="Specify the job title to apply for")],
    jobName: Annotated[List[str], typer.Option(["--title-name", "--jtn"], help="Specify the job title name to apply for")],
    jobBoardId: Annotated[int, typer.Option(["--board-id", "-jbid"], help="Specify the job board id to use for search")],
    jobBoardName: Annotated[List[str], typer.Option(["--board-name", "-jbn"], help="Specify the job board name to use for search")],
    useEasyApplyOnly: Annotated[bool, typer.Option(["--easy-only", "-e"], help="Specifies if job search should only use the easy apply feature on the job board")] = False,
    runType: Annotated[ScheduleType, typer.Option(["--run-type", "-rt"], case_sensitive=False, help="Sets the interval for schedule job search to run, defaults to Once")] = ScheduleType.ONCE
) -> None:
    """Create a scheduled job search runs automatically on specified schedule using crontab, can be set to run once, daily, weekly, monthlly"""
    bcontroller = get_controller()
    jtid = None
    jbid = None
    if jobName and not jobTitleId:
        jobTitle = bcontroller.getJobTitleByName("".join(jobName))
        if not jobTitle.item:
            typer.secho(f"Command failed, no job title found with name '{jobName}', please enter valid job title name or id", fg=typer.colors.RED)
        else:
            jtid = jobTitle.item["id"]
    elif not jobName and jobTitleId:
        jobTitle = bcontroller.getJobtitle(jobTitleId)
        if not jobTitle.item:
            typer.secho(f"Command failed, no job title found with id '{jobTitleId}', please enter a valid job title name or id", fg=typer.colors.RED)
    if jobBoardName and not jobBoardId:
        jobBoard = bcontroller.getJobBoardByName("".join(jobBoardName))
        if not jobBoard.item:
            typer.secho(f"Command faild, no job board found with name '{jobBoardName}', please enter a valid job board name or id", fg=typer.colors.RED)
        else:
            jbid = jobBoard.item["id"]
    elif not jobBoardName and jobBoardId:
        jobBoard = bcontroller.getJobBoard(jobBoardId)
        if not jobBoard.item:
            typer.secho(f"Command failed, no job board found with id '{jobBoardId}, please enter a valid job board name or id", fg=typer.colors.RED)
    if not jobTitleId and not jobName:
        typer.secho("You must specifiy either a job title name or job title id", fg=typer.colors.RED)
    if not jobBoardId and not jobBoardName:
        typer.secho("You must specify either a job board name or job board id")
    scheduledRun, exCode = bcontroller.addScheduleRun(
        name,
        jobTitleId=jtid if jobName else jobTitleId,
        jobBoardId=jbid if jobBoardName else jobBoardId,
        onlyEasyApply=1 if useEasyApplyOnly else 0,
        runType=runType
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
        stable = get_singlerow_table(**scheduledRun)
        print_table(stable)


@app.command()
#needs name,runDay,runDayOfWeek,runHr,runMin,durMin,numbSubmissions
# TODO if initial start is different than the day of week then use day of week instead of datetime day
def enableScheduledSearch(
    name: Annotated[List[str], typer.Argument(..., help="Name of a previously created scheduled search")],
    runDateTime: Annotated[
        datetime, 
        typer.Argument(
            ...,
            help="The date and time of the initial run", 
            formats=["%d/%m/%Y%H:%M", "%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M"]
        )],
    runDayOfWeek: Annotated[WeekDays, typer.Option(["--week-day", "-wd"], help="Specifies the day of the week scheduled search should occur on")]=None,
    runMonth: Annotated[Months, typer.Option(["--month", "-m"], help="Sets the month schedule search should run")]=None,
    durrationMinutes: Annotated[int, typer.Option(["--dur-mins", "-m"], help="Sets the the length of time in minutes the search runs")]=30,
    numberOfSubmissions: Annotated[int, typer.Option(["--submissions", "-s"], help="Indicates the number of submissions the search should complete before exiting")]=None,
    everyHours: Annotated[int, typer.Option(["--every-hours", "-eh"], help="Sets the scheduled search to run every x hours")]=None,
    everyMins: Annotated[int, typer.Option(["--every-mins", "-em"], help="Sets the scheduled search to run every x minutes")]=None,
    repeat: Annotated[bool, typer.Option(["--repeat", "-r"], help="Indicates if the scheduled search should repeat or not, defaults to TRUE")]=True

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
    
    run_date = RunDate(
        monthDay = runDateTime.weekday() if not runDayOfWeek else get_weekday_int(runDayOfWeek), 
        weekDay = runDateTime.day, 
        month = runDateTime.month if not runMonth else runMonth, 
        hour = runDateTime.hour, 
        minute = runDateTime.minute, 
        everyHr = everyHours,
        everyMin = everyMins, 
        repeat = repeat
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
    stable = get_singlerow_table(**scheduledRun)
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
    everyHour: Annotated[int, typer.Option(["--every-hour", "-eh"], help="Sets the scheduled search to run every x hours")],
    everyMin: Annotated[int, typer.Option(["--every-min", "-em"], help="Sets the scheduled search to run every x minutes")],
    durrationMin: Annotated[int, typer.Option(["--durration", "-d"], help="Sets the durration of the search in minutes, defaults to 30")]=30,
    numberOfSubs: Annotated[int, typer.Option(["--number-submissions", "-ns"], help="Sets the number of submissions for search to complete before exiting")]=None
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
    stable = get_singlerow_table(**scheduledRun)
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
    everyHour: Annotated[int, typer.Option(["--every-hour", "-eh"], help="Sets the search to run every x hours")],
    everyMin: Annotated[int, typer.Option(["--every-min", "-em"], help="Sets the search to run every x minutes")],
    durrationMin: Annotated[int, typer.Option(["--durration", "-d"], help="Sets the durration of the search in minutes, defatuls to 30")]=30,
    numberOfSubs: Annotated[int, typer.Option(["--number-submissions", "-ns"], help="Sets the number of submissions for search to complete before exiting")]=None
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
    stable = get_singlerow_table(**scheduledRun)
    print_table(stable)    


@app.command()
def enableMontlyScheduledSearch():
    """Enable a schedule search to run montly on a specific day and time"""
    typer.secho(
        "Enable monthly schedule not implemented yet",
        fg=typer.colors.YELLOW
    )
    pass


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