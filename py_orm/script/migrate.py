import os
import re
import json
from os.path import join
from typing import TypedDict

from typer import Typer, confirm, echo

from py_orm import BaseModel
from py_orm.migrations.main import migrations


class MetadataFile(TypedDict):
    number_file: int
    number_migrate: int


app = Typer()


@app.command()
def create(yes: bool = False):
    if not (BaseModel.__config_py_orm__['migrate_dir'] in os.listdir(path=".")):
        os.mkdir(BaseModel.__config_py_orm__['migrate_dir'])
    if not ('py_orm.json' in os.listdir(path=BaseModel.__config_py_orm__['migrate_dir'])):
        with open(
            join(
                BaseModel.__config_py_orm__['migrate_dir'],
                'py_orm.json')
            , 'w'
        ) as file:
            json.dump({
                'number_file': 0,
                'number_migrate': 0,
            }, file)

    migrate_files = os.listdir(path=BaseModel.__config_py_orm__['migrate_dir'])

    migrate_run, migrate_rollback = migrations()

    metadata_file: MetadataFile
    with open(
            join(
                BaseModel.__config_py_orm__['migrate_dir'],
                'py_orm.json')
            , 'r'
    ) as file:
        metadata_file = json.load(file)

    if metadata_file['number_migrate'] < len(migrate_files) - 1 and not yes:
        abort = confirm(f"overwrite file <{metadata_file['number_file']}.sql>?", abort=True)
        if not abort:
            return

    with open(
            join(
                BaseModel.__config_py_orm__['migrate_dir'],
                f"{metadata_file['number_file']}.sql"
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
