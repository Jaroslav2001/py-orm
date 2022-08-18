import os
import re
import json
from os.path import join
from typing import TypedDict, Dict, Tuple

from typer import Typer, confirm

from py_orm import BaseModel
from py_orm.migrations.main import migrations, execute


class MetadataFile(TypedDict):
    number_file: int
    number_migrate: int


app = Typer()


def get_metadata_file() -> MetadataFile:
    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                'py_orm.json'
            ), 'r'
    ) as file:
        return json.load(file)


def set_metadata_file(value: MetadataFile):
    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                'py_orm.json'
            ), 'w'
    ) as file:
        json.dump(value, file)


def create_dir():
    if not (BaseModel.__config_py_orm__.migrate_dir in os.listdir(path=".")):
        os.mkdir(BaseModel.__config_py_orm__.migrate_dir)
    if not ('py_orm.json' in os.listdir(path=BaseModel.__config_py_orm__.migrate_dir)):
        set_metadata_file(
            {
                'number_file': 0,
                'number_migrate': 0,
            }
        )


def get_sql_file(number: int):
    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                f"{number}.sql"
            ), 'r'
    ) as file:
        return file.read()


@app.command()
def create(yes: bool = False):
    create_dir()

    migrate_files = os.listdir(path=BaseModel.__config_py_orm__.migrate_dir)

    migrate_run, migrate_rollback = migrations()

    metadata_file = get_metadata_file()

    if metadata_file['number_file'] < len(migrate_files) - 1 and not yes:
        abort = confirm(f"overwrite file <{metadata_file['number_file']}.sql>?", abort=True)
        if not abort:
            return

    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                f"{metadata_file['number_file']}.sql"
            ), 'w'
    ) as file:
        for i, sql_command in enumerate(migrate_run):
            file.write(f"-- <migrate {i}>\n{sql_command}\n\n")

        file.write('\n')
        migrate_rollback.reverse()

        for i, sql_command in enumerate(migrate_rollback):
            file.write(f"-- <rollback {i}>\n{sql_command}\n\n")

    metadata_file['number_file'] += 1
    set_metadata_file(metadata_file)


# Parsing sql migrate file
# -- *(<(?:migrate|rollback) *[0-9]+> *\n[\s\w(),]*;)
# <((?:migrate|rollback)) *([0-9]+)> *\n([\s\w(),]*;)


@app.command()
def run():
    metadata_file = get_metadata_file()

    sql_commands: Tuple[str, ...] = re.search(
        r"-- *(<(?:migrate|rollback) *\d+> *\n[\s\w(),]*;)",
        get_sql_file(metadata_file['number_file'])
    ).groups()

    sql_commands_run: Dict[int, str] = {}
    sql_commands_rollback: Dict[int, str] = {}

    for sql_command in sql_commands:
        sql_command = re.search(
            r"<((?:migrate|rollback)) *(\d+)> *\n([\s\w(),]*;)",
            sql_command
        ).groups()

        if sql_command[0] == 'migrate':
            sql_commands_run[int(sql_command[1])] = sql_command[2]
        if sql_command[0] == 'rollback':
            sql_commands_rollback[int(sql_command[1])] = sql_command[2]

        for sql in sql_commands_run.values():
            execute(sql)


@app.command()
def rollback():
    pass
