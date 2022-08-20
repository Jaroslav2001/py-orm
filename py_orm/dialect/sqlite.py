from typing import TYPE_CHECKING

from .abstract import DialectSQL, ConvertType, TypesConvert

if TYPE_CHECKING:
    from py_orm.migrations.migrations_model import MigrationsModel


def schema_parsing() -> 'MigrationsModel':
    pass


sqlite = DialectSQL(
    list_table="SELECT name FROM sqlite_schema WHERE type == 'table';",
    schema_table="SELECT sql FROM sqlite_schema WHERE type == 'table' AND name = {name};",
    create_table='CREATE TABLE',
    alter_table='ALTER TABLE',
    drop_table='DROP TABLE',
    schema_parsing=schema_parsing,
    types=TypesConvert(
        int=ConvertType(int, 'INTEGER', lambda x: x),
        float=ConvertType(float, 'REAL', lambda x: x),
        str=ConvertType(str, 'TEXT', lambda x: f"'{x}'"),
        bool=ConvertType(bool, 'INT', lambda x: '1' if x else '0'),
        bytes=ConvertType(bytes, 'BLOB', lambda x: x),
    ),

    primary_key='PRIMARY KEY',
    foreign_key='foreign_key',
    unique='UNIQUE',
    index='INDEX',
    auto_increment='AUTOINCREMENT',

    not_null='NOT NULL',
    null='NULL',
)
