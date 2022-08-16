from typing import TypedDict, Callable


class DialectSQL(TypedDict):
    list_table: str
    schema_table: str
    create_table: str
    alter_table: str
    drop_table: str
