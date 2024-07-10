"""
This module provides the Bojo CLI
# bojo/cli.py
"""
from pathlib import Path
from typing import Optional
import typer
from bojojo import ERRORS, __app_name__, __version__
from bojojo.src import config, db_config
from bojojo.repositories import db_init

app = typer.Typer()

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