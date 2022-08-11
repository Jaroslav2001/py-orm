from typing import TypedDict


class DialectSQL(TypedDict):
    schema_table: str
    create_table: str
    alter_schema: str
    drop_schema: str
