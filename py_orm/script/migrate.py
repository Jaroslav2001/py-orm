from os import mkdir
from os.path import join

from typer import Typer


app = Typer()


@app.command()
def init(import_: str, mkdir_name: str = 'migrations', ):
    with open('manage.py', 'w') as file:
        file.write(f'import {mkdir_name}\n')
    mkdir(mkdir_name)

    with open(join(mkdir_name, '__init__.py'), 'w') as file:
        file.write('')


@app.command()
def create(import_: str):
    pass


@app.command()
def run(import_: str):
    pass
