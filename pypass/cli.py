from pathlib import Path
from typing import Optional
import typer

from pypass import ERRORS, __app_name__, __version__, config, database, controller
from pypass import SUCCESS

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "--db",
        prompt="pypass database location?"
    )) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The pypas database is {db_path}", fg = typer.colors.GREEN)

def get_pypasmanager() -> controller.PyPassManager:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        key = database.get_key(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return controller.PyPassManager(db_path, key)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    username: str = typer.Argument(""),
    password: str = typer.Option("", "--password", "-p"),
    website_address: str = typer.Option("", "--website", "-w")
    ) -> None:
    pypass = get_pypasmanager()
    if username == "" or password == "" or website_address == "":
        typer.secho(
            'Please fill all the requirement',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    status, _ = pypass.register_passdata(username, password, website_address)
    if status == SUCCESS:
        typer.secho(
            f"PyPass: {username} successfully registered",
            fg=typer.colors.GREEN
        )
    else:
        typer.secho(
            'Failed to register',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def get(
    page: int = typer.Argument(0),
    decrypt: bool = typer.Option(
        False,
        "--decrypt",
        "-d",
        help="Decrypt the stored pass data"
    )) -> None:
    pypass = get_pypasmanager()
    status, data = pypass.get_all_passdata(page, decrypt)
    if status == SUCCESS:
        typer.secho(
            "PyPass: successfully fetch",
            fg=typer.colors.GREEN
        )
        for dat in data:
            typer.secho(
                f"| {dat[0]} | {dat[1]} | {dat[2]} | {dat[3]} |",
                fg=typer.colors.CYAN
            )
    else:
        typer.secho(
            'Failed to fetch data',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def search(
    page: int = typer.Argument(0),
    username: str = typer.Option("", "--username", "-u"),
    website_address: str = typer.Option("", "--website", "-w"),
    decrypt: bool = typer.Option(
        False,
        "--decrypt",
        "-d",
        help="Decrypt the stored pass data"
    )) -> None:
    pypass = get_pypasmanager()
    status, data = pypass.search_passdata(username, website_address, page, decrypt)
    if status == SUCCESS:
        typer.secho(
            "PyPass: successfully fetch",
            fg=typer.colors.GREEN
        )
        for dat in data:
            typer.secho(
                f"| {dat[0]} | {dat[1]} | {dat[2]} | {dat[3]} |",
                fg=typer.colors.CYAN
            )
    else:
        typer.secho(
            'Failed to fetch data',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def update(
    pass_id: str = typer.Argument(""),
    username: str = typer.Option("", "--username", "-u"),
    password: str = typer.Option("", "--password", "-p"),
    website_address: str = typer.Option("", "--website", "-w")
    ) -> None:
    pypass = get_pypasmanager()
    if pass_id == "" or username == "" or password == "" or website_address == "":
        typer.secho(
            'Please fil all the requirement',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    status, _ = pypass.update_passdata(pass_id, username, password, website_address)
    if status == SUCCESS:
        typer.secho(
            f"PyPass: successfully update {username} data",
            fg=typer.colors.GREEN
        )
    else:
        typer.secho(
            'Failed to update',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def delete(
    pass_id: str = typer.Argument(""),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation",
    )) -> None:
    pypass = get_pypasmanager()

    def _remove():
        status, _ = pypass.delete_passdata(pass_id)
        if status == SUCCESS:
            typer.secho(
                f"Pass data #{pass_id} successfully removed",
                fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                f"Pass data #{pass_id} failed to remove",
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
    if force:
        _remove()
    else:
        _, data = pypass.get_passdata(pass_id)
        confirm_delete = typer.confirm(
            f"Deleting #{pass_id}: {data[1]} - {data[2]}"
        )
        if confirm_delete:
            _remove()
        else:
            typer.echo("Operation Canceled")

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
        help="Show the application's version.",
        callback=_version_callback,
        is_eager=True,
    )) -> None:
    return