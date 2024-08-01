"""
This module provides the Bojo CLI
# bojo/cli.py
"""
import datetime
from pathlib import Path
from typing import Annotated, List, Optional
import typer
from bojojo import CONFIG_FILE_PATH, ERRORS, SUCCESS, __app_name__, __version__
from bojojo.controllers.bojo_controller import BojoController
from bojojo.src import config, db_config
from bojojo.repositories import db_init
from bojojo.inject_config import base_config
from rich.console import Console

from bojojo.types.days import WeekDays
from bojojo.types.schedule_types import ScheduleType
from bojojo.utils.cli_tables import get_multirow_table, get_singlerow_table


app = typer.Typer()

#TODO remove abilities to add alternate db path
@app.command()
def init(
    db_path: str = typer.Option(
        str(db_config.DEFAULT_DB_FILE_PATH),
        "--db_path",
        "--dbp",
        prompt="Enter location for Bojo database (press enter to keep default loc):",
    ),
) -> None:
    """Initialize Bojo database and create tables"""
    app_init_err = config.init_app(db_path)
    if app_init_err:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_err]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_err = db_init.initialize_db(Path(db_path))
    if db_init_err:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_err]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Bojo database created successfully at {db_path}", fg=typer.colors.GREEN)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

def get_controller() -> BojoController:
    if CONFIG_FILE_PATH.exists():
        db_path = db_config.get_database_path(CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "bojojo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return BojoController(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "bojojo init"',
            fg=typer.colors.RED
        )

def get_console() -> Console:
    return Console()


@app.command
def add_job_board(
    name: Annotated[List[str], typer.Argument(help="Enter name of a job board to apply for jobs")],
    url: Annotated[str, typer.Argument(help="Enter the url for the job board")],
    has_easy_apply: Annotated[Optional[bool], typer.Option("--easy", "-e", help="Indicates the job board has a easy apply feature")]
) -> None:
    """Add a new job board that can be used to apply for jobs"""
    bcontroller = get_controller()
    has_easy = 1 if has_easy_apply else 0
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
        console = get_console()
        console.print(jbtable)


@app.command
def update_job_board(
    name: Annotated[List[str], typer.Option(help="Name of job board to update")],
    id: Annotated[int, typer.Option(help="Id of job board to update")],
    url: Annotated[str, typer.Option(help="Url for job board")],
    has_easy_apply: Annotated[Optional[bool], typer.Option("--easy", "-e", help="Indicates if the job board has a easy apply feature")]
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
        console = get_console()
        console.print(jtable)


@app.command
def add_resume(
        name: Annotated[List[str], typer.Argument("--name", "-n", help="Enter a name to help identify saved resumes")],
        job_id: Annotated[int, typer.Argument("--job-id", "-jid", help="Job id will link a resume to a specific job")],
        file_path: Annotated[str, typer.Argument("--file-path", "-fp", help="The file path where the resume can be found")]
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
        console = get_console()
        console.print(rtable)
    

#TODO update resume to update based off name not id
@app.command
def update_resume(
    name: Annotated[List[str], typer.Option("--name", '-n', help="Update resume name")],
    job_id: Annotated[int, typer.Option("--job-id", "-jid", help="Update job id to use resume with a different job")],
    file_path: Annotated[str, typer.Option("--file-path", '-fp', help="Update resume to point to a different file location")]
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
        console = get_console()
        console.print(rtable)


@app.command
def remove_resume(
    name: Annotated[List[str], typer.Option("--name", "-n", help="Name of resume to delete")],
    all: Annotated[bool, typer.Option("--all", "-a", help="Delete all saved resumes")]
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
        console = get_console()
        console.print(rtable)


#TODO note date times can be used on dt values from typer cli arg types
#TODO might have to update experience years in service cls
@app.command
def add_job_title(
    name: Annotated[List[str], typer.Argument("--name", '-n', help="Enter the name of a job title to apply for")],
    experience_years: Annotated[float, typer.Argument("--xp-years", '-y', help="The years of experience for job title, value will be used in job search")],
    experience_level: Annotated[str, typer.Argument('--xp-level', '-l', help="Experience level for job title, exepted values 'junior, mid, and senior'")]
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
        console = get_console()
        console.print(ttable)
        

@app.command
def update_job_title(
    job_id: Annotated[int, typer.Option("--jid", "-id", help="Specifies the id of the job title to change")],
    name: Annotated[List[str], typer.Option("--name", "-n", help="Change the name of a saved job title")],
    experience_years: Annotated[float, typer.Option("--xp-years", "-y", help="Update the years of experience for a job title")],
    experience_level: Annotated[str, typer.Option("--xp-level", "-l", help="Update the level of experience for a job title, expected values 'junior, mid, senior'")]
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
        console = get_console()
        console.print(ttable)


#TODO need to add a delete by name method and update name of current delete method
@app.command
def remove_job_title(
    name: Annotated[List[str], typer.Option("--name", "-n", help="Specifies the name of a job title to delete")],
    job_id: Annotated[int, typer.Option("--job-title-id", "-jti", help="Specifies the id of a job title to delete")],
    all: Annotated[bool, typer.Option("--all", "-a", help="Delete all saved job titles")]
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
        console = get_console()
        console.print(jTable)


@app.command
#needs name,jobTitleId,jobBoardId,runType,easyApplyOnly
def addScheduledSearch(
    name: Annotated[List[str], typer.Argument("--name", "-n", help="Specify a name to identify a scheduled search")],
    jobTitleId: Annotated[int, typer.Option("--title-id", "-jtid", help="Specify the job title to apply for")],
    jobName: Annotated[List[str], typer.Option("--title-name", "--jtn", help="Specify the job title name to apply for")],
    jobBoardId: Annotated[int, typer.Option("--board-id", "-jbid", help="Specify the job board id to use for search")],
    jobBoardName: Annotated[List[str], typer.Option("--board-name", "-jbn", help="Specify the job board name to use for search")],
    useEasyApplyOnly: Annotated[bool, typer.Option("--easy-only", "-e", help="Specifies if job search should only use the easy apply feature on the job board")] = False,
    runType: Annotated[ScheduleType, typer.Option("--run-type", "-rt", case_sensitive=False, help="Sets the interval for schedule job search to run, defaults to Once")] = ScheduleType.ONCE
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
        console = get_console()
        console.print(stable)


@app.command
#needs name,runDay,runDayOfWeek,runHr,runMin,durMin,numbSubmissions
def enableScheduledSearch(
    name: Annotated[List[str], typer.Argument("--name", "-n", help="Name of a previously created scheduled search")],
    runTDateTime: Annotated[
        datetime, 
        typer.Argument(
            "--run-dt", "-rdt", 
            help="The date and time of the initial run", 
            formats=["%d/%m/%Y%H:%M", "%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M"]
        )],
    runDayOfWeek: Annotated[WeekDays, typer.Option("--week-day", "-wd", help="Specifies the day of the week scheduled search should occur on")]=WeekDays.MON,
    durrationMinutes: Annotated[int, typer.Option("--dur-mins", "-m", help="Sets the the length of time in minutes the search runs")]=30,
    numberOfSubmissions: Annotated[int, typer.Option("--submissions", "-s", help="Indicates the number of submissions the search should complete before exiting")]=None,
    everyHours: Annotated[int, typer.Option("--every-hours", "-eh", help="Sets the scheduled search to run every x hours")]=None,
    everyMins: Annotated[int, typer.Option("--every-mins", "-em", help="Sets the scheduled search to run every x minutes")]=None
) -> None:
    """Enables previous scheduled searches to automatically run at a set date and time, certain days of weeks, certain days of the month, every x amount of hours, or every x amount of minutes"""
    pass


# for these next 3 commands pass in a date time and then a day of week or day of month have opt for every hour/mins
@app.command
def addDailyScheduledSearch():
    pass


@app.command
def addWeeklyScheduledSearch():
    pass


@app.command
def addMontlyScheduledSearch():
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