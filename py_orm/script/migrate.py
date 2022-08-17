import os
from os.path import join

from typer import Typer

from py_orm import BaseModel

app = Typer()


@app.command()
def create():
    if not(BaseModel.__config_py_orm__['migrate_dir'] in os.listdir(path=".")):
        os.mkdir(BaseModel.__config_py_orm__['migrate_dir'])
    migrate_files = os.listdir(path=BaseModel.__config_py_orm__['migrate_dir'])


@app.command()
def run():
    pass


@app.command()
def rollback():
    pass
