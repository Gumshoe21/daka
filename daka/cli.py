"""This module provides the Daka CLI."""

from pathlib import Path
from typing import Optional

import typer
import json

from daka import timer, ERRORS, __app_name__, __version__, config, database, daka

app = typer.Typer()

# Retrieves the Daka object for use in commands


def get_daka() -> daka.Daka:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "daka init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return daka.Daka(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


# init
@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="Daka database location?",
    ),
) -> None:
    """Initialize the Daka database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Create config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Create database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The Daka database is {db_path}", fg=typer.colors.GREEN)


# add
def mode_callback(value: str):
    if str(value) not in ["1", "2", "3"]:
        raise typer.BadParameter("Invalid input: please choose 1, 2, or 3.")
    else:
        return value


@app.command()
def add(
    mode: str = typer.Option(
        prompt="Please choose a mode: \n1 for countdown, \n2 for stopwatch, \n3 for pomodoro\nYour choice",
        callback=mode_callback,
    ),
    name: str = typer.Argument(),
    duration: int = typer.Argument(),
):
    daka = get_daka()

    modes = {"1": "countdown", "2": "stopwatch", "3": "pomodoro"}
    timer, error = daka.add(modes[mode], name, duration)
    if error:
        typer.secho(f'Adding timer faciled with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"You've added a new timer:\nName: {timer['name']}\nMode: {timer['mode']}\nDuration: {timer['duration']} was added ",
            fg=typer.colors.GREEN,
        )


# run
@app.command()
def run(name: str) -> None:
    t = timer.Stopwatch("my timer", 60)
    t.start()
    daka = get_daka()


# list
@app.command()
def list():
    daka = get_daka()
    for t in daka.list():
        # for k, v in t.items():
        #    print(f"{k.capitalize()}:{v}")
        print(f"{t['name']}")


# TODO add list by mode
# TODO add list by duration threshold


# main
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
        help="Show Daka version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
