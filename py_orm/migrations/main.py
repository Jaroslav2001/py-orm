import os
import re
from os.path import join
import json

from typer import confirm

from typing import NoReturn, TypedDict, Tuple

from py_orm import BaseModel
from py_orm.old_sql_builder.migrate import Database

metadata: str = 'py_orm.json'


class MetadataFile(TypedDict):
    number_file: int
    number_migrate: int


def get_metadata_file() -> MetadataFile:
    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                metadata
            ), 'r'
    ) as file:
        return json.load(file)


def set_metadata_file(value: MetadataFile):
    with open(
            join(
                BaseModel.__config_py_orm__.migrate_dir,
                metadata
            ), 'w'
    ) as file:
        json.dump(value, file)


def create_dir():
    if not (BaseModel.__config_py_orm__.migrate_dir in os.listdir(path=".")):
        os.mkdir(BaseModel.__config_py_orm__.migrate_dir)
    if not (metadata in os.listdir(path=BaseModel.__config_py_orm__.migrate_dir)):
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


def execute(sql: str, *args, **kwargs) -> NoReturn:
    if BaseModel.__config_py_orm__.async_:
        # Create execute async_
        pass
    else:
        from py_orm.driver.sync import connect, TConnection

        with connect() as connect_:
            connect_: TConnection
            cursor = connect_.cursor()
            cursor.execute(sql, *args, **kwargs)
            connect_.commit()


def create_sql_migrate(yes: bool):
    create_dir()

    migrate_files = os.listdir(path=BaseModel.__config_py_orm__.migrate_dir)

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
        file.write(Database().__sql__())


def migrate(rollback: bool = False):
    mode = 'migrate'
    if rollback:
        mode = 'rollback'

    metadata_file = get_metadata_file()

    sql_commands: Tuple[str, ...] = re.search(
        r"--.*<start>\n([\w\s(),;-]*)--.*<end>",
        get_sql_file(metadata_file['number_file'] - 1
                     if rollback else
                     metadata_file['number_file']
                     )
    ).groups()

    if rollback:
        sql_commands = sql_commands[::-1]

    for sql_command in sql_commands:
        sql_command = re.search(
            r"(--.*(?:migrate|rollback)\n[\w\s(),-]*;)\s(--.*(?:migrate|rollback)\n[\w\s(),-]*;)",
            sql_command
        ).groups()

        for content in sql_command:
            key, value = re.search(
                r"--.*(migrate|rollback)\n([\w\s(),-]*;)",
                content,
            ).groups()

            if key == mode:
                execute(value)
        if mode == 'migrate':
            metadata_file['number_migrate'] += 1
        else:
            metadata_file['number_migrate'] -= 1

    metadata_file['number_migrate'] = 0
    if mode == 'migrate':
        metadata_file['number_file'] += 1
    else:
        metadata_file['number_file'] -= 1

    set_metadata_file(metadata_file)
