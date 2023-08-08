import os
import subprocess
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from rich import print
import typer

from templates import Writer


project_name = "express-docker-typescript-starter-kit"
branch_name = "socket-and-mongo-listener"
github_repo_url = f"https://github.com/j0rdiC/{project_name}"


app = typer.Typer()


def cmd(command: str | list[str], **kwargs) -> subprocess.CompletedProcess:
    try:
        command = command.split() if type(command) is str else command
        return subprocess.run(command, check=True, **kwargs)
    except subprocess.CalledProcessError as e:
        print(e)
        raise typer.Exit()


@app.command()
def init(
    project_path: Annotated[Path, typer.Argument(help="Project path")] = Path.cwd() / 'server',
    intall_deps: Annotated[bool, typer.Option('-i', '--install', help="Install dependencies")] = False
):
    cmd(f"git clone --single-branch --branch {branch_name} {github_repo_url} {project_path}")
    os.chdir(project_path)
    cmd('rm -rf .git')
    cmd('git init')
    cmd('git add .')
    cmd(['git', 'commit', '-m', 'Initial commit'], stdout=subprocess.DEVNULL)
    if intall_deps:
        subprocess.run(['npm', 'install'])
    print(f"\n[green]✓[/] Project [blue]{project_path}[/] created successfully")


@app.command()
def route(
    name: str,
    methods: Annotated[Optional[list[str]], typer.Argument(help="Add specific http methods")] = None,
    with_model: Annotated[bool, typer.Option('-m', '--model', help="Create a model")] = False,
    with_handler: Annotated[bool, typer.Option('-h', '--handler', help="Use the generic route handler")] = False,
):
    if with_handler and not with_model:
        print("The --handler option must be used with the --model option")
        raise typer.Exit()

    writer = Writer(name, with_model, with_handler)
    writer.write(methods)
    print(f"Route '{name}' created successfully [green]✓[/] ")


@app.command()
def model(name: str):
    print(name)


if __name__ == "__main__":
    app()
