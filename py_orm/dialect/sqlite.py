from typing import Type, Union, Tuple

from .abstract import DialectSQL, ConvertType

from py_orm.migrations.migrations_model import MigrationsModel


def schema_parsing() -> 'MigrationsModel':
    pass


sqlite: DialectSQL = {
    'list_table': "SELECT name FROM sqlite_schema WHERE type == 'table';",
    'schema_table': "SELECT sql FROM sqlite_schema WHERE type == 'table' AND name = {name};",
    'create_table': 'CREATE TABLE',
    'alter_table': 'ALTER TABLE',
    'drop_table': 'DROP TABLE',
    'schema_parsing': schema_parsing,
    'types': (
        ConvertType[int](int, 'INTEGER'),
        ConvertType[float](float, 'REAL'),
        ConvertType[str](str, 'TEXT'),
        ConvertType[bool](bool, 'INT'),
        ConvertType[bytes](bytes, 'BLOB'),
    )
}
