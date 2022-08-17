import os
import re
from os.path import join

from typer import Typer

from py_orm import BaseModel
from py_orm.migrations.main import migrations

app = Typer()


@app.command()
def create():
    if not (BaseModel.__config_py_orm__['migrate_dir'] in os.listdir(path=".")):
        os.mkdir(BaseModel.__config_py_orm__['migrate_dir'])
    migrate_files = os.listdir(path=BaseModel.__config_py_orm__['migrate_dir'])

    migrate_run, migrate_rollback = migrations()

    with open(
            join(
                BaseModel.__config_py_orm__['migrate_dir'],
                f"{len(migrate_files)}.sql"
            ), 'w'
    ) as file:
        for i, sql_command in enumerate(migrate_run):
            file.write(f"-- <migrate {i}>\n{sql_command}\n\n")

        file.write('\n')
        migrate_rollback.reverse()

        for i, sql_command in enumerate(migrate_rollback):
            file.write(f"-- <rollback {i}>\n{sql_command}\n\n")


# Parsing sql migrate file
# -- *(<(?:migrate|rollback) *[0-9]+> *\n[\s\w(),]*;)
# <((?:migrate|rollback)) *([0-9]+)> *\n([\s\w(),]*;)


@app.command()
def run():
    pass


@app.command()
def rollback():
    pass
