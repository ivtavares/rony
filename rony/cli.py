import click
import os
import re
import sys
from .writer import *
from .__init__ import __version__ as version

LOCAL_PATH = os.getcwd()

logo = r"""

 _ __ ___  _ __  _   _ 
| '__/ _ \| '_ \| | | |
| | | (_) | | | | |_| |
|_|  \___/|_| |_|\__, |
                 |___/ 
v{}
""".format(version)

@click.group()
def cli():
    pass

@cli.command()
def info():
    """
    Checks that Rony is correctly installed
    """
    click.echo(logo)


@cli.command()
@click.argument('project_name')
@click.option('-imp', '--implemented', 'implemented', prompt='Do you want to start with an implemented example (recommended) [y/n]?', 
            default='y', show_default=True)
def new(project_name, implemented):
    """
    Create a new Rony project
    """
    if implemented in ['yes', 'ye', 'y', 'Yes', 'YES', 'Y']:
        file_source = 'file_text'
    elif implemented in ['no', 'n', 'No', 'NO', 'N']:
        file_source = 'not_implemented_file_text'
    
    click.echo(f"Creating project {project_name}")
    # Create project folders
    os.makedirs(os.path.join(LOCAL_PATH, project_name, 'etl'))
    os.makedirs(os.path.join(LOCAL_PATH, project_name, 'dags'))
    os.makedirs(os.path.join(LOCAL_PATH, project_name, 'scripts'))
    os.makedirs(os.path.join(LOCAL_PATH, project_name, 'infrastructure'))
    os.makedirs(os.path.join(LOCAL_PATH, project_name, 'tests'))
    os.makedirs(os.path.join(LOCAL_PATH, project_name, '.github/workflows'))

    # Write files
    # ...

    print(f'Creating virtual environment {project_name}_env')
    os.chdir(project_name)
    env_name = f"{project_name}_env"
    os.system(f"python -m venv {env_name}")

    # Create git repo
    os.system('git init')
    print("A git repository was created. You should add your files and make your first commit.\n")
    


@click.argument('image_name')
@cli.command()
def build(image_name):
    """
    Build a docker image with given image_name. Only run if you have docker installed.
    One should be at the root directory.
    """
    if not os.path.exists('Dockerfile'):
        click.echo("You gotta have a Dockerfile file.")
    else:
        os.system(f'docker build -t {image_name} .')


@click.argument('image_name')
@cli.command()
def run(image_name):
    """
    Run a container with given image_name. 
    Only run if you have docker installed.
    """
    if not os.path.exists('Dockerfile'):
        click.echo("You gotta have a Dockerfile file")
    else:
        os.system(f'docker run --rm -p 5000:5000 {image_name}')