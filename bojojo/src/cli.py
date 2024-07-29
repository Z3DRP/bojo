"""
This module provides the Bojo CLI
# bojo/cli.py
"""
from pathlib import Path
from typing import Annotated, List, Optional
import typer
from bojojo import CONFIG_FILE_PATH, ERRORS, SUCCESS, __app_name__, __version__
from bojojo.controllers.bojo_controller import BojoController
from bojojo.src import config, db_config
from bojojo.repositories import db_init
from bojojo.inject_config import base_config
from rich.console import Console

from bojojo.utils.cli_tables import get_singlerow_table


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


@app.command()
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
    name: Annotated[List[str], typer.Option("--name", "-n", help="Change the name of a saved job title")],
    experience_years: Annotated[float, typer.Option("--xp-years", "-y", help="Update the years of experience for a job title")],
    experience_level: Annotated[str, typer.Option("--xp-level", "-l", help="Update the level of experience for a job title, expected values 'junior, mid, senior'")]
) -> None:
    """Update a job title to apply for"""
    bcontroller = get_controller()
    updatedJob, exCode = bcontroller.modifyJobTitle(name, experienceYrs=experience_years, experienceLvl=experience_level)
    if exCode != SUCCESS:
        typer.secho(
            f'Updating job title {name} failed with "{ERRORS[exCode]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Job title: {updatedJob['name']} was updated successfully"
        )
        ttable = get_singlerow_table(**updatedJob)
        console = get_console()
        console.print(ttable)


#TODO need to add a delete by name method and update name of current delete method
@app.command
def remove_job_title(
    name: Annotated[List[str], typer.Option("--name", "-n", help="Specifies the name of a job title to delete")],
    job_id: Annotated[int, typer.Option("--job-title-id", "-jti", help="Specifies the id of a job title to delete")]
) -> None:
    """Delete a job title using the name or id"""
    bcontroller = get_controller()
    deletedJob = None
    
    if name and not job_id:
        deletedJob, exCode = bcontroller.removeJobTitleByName(name)
    elif job_id and not name:
        deleteByVal = name if name is not None else job_id
        deletedJob, exCode = bcontroller.removeJobTitleById(job_id)
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
            f"Job title: {deletedJob['name']} was deleted successfully"
        )




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