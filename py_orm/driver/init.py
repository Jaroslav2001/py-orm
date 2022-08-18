from typing import (
    TYPE_CHECKING,
    Literal,
    Union,
    Tuple,
    TypeAlias,
    Type,
)

if TYPE_CHECKING:
    from py_orm.driver.sync import TCursor, TConnection
    from py_orm.driver.async_ import (
        TCursor as TCursorAsync,
        TConnection as TConnectionAsync,
    )

Driver: TypeAlias = Literal[
    "sqlite3", "pymysql", "psycopg2", "asyncpg", "aiomysql", "aiosqlite",
]


def is_async(driver: Driver) -> bool:
    if driver in ("sqlite3", "pymysql", "psycopg2"):
        return False
    if driver in ("asyncpg", "aiomysql", "aiosqlite"):
        return True
    print(f'lol {driver}')


def get_driver(driver: Driver) -> Tuple[
    Union[Type['TConnection'], Type['TConnectionAsync'], Type],
    Union[Type['TCursor'], Type['TCursorAsync'], Type]
]:
    if driver == "sqlite3":
        from sqlite3 import Connection, Cursor
        return Connection, Cursor
    if driver == "pymysql":
        from pymysql import Connection
        from pymysql.cursors import Cursor
        return Connection, Cursor
    if driver == "psycopg2":
        from psycopg2._psycopg import ReplicationConnection, ReplicationCursor
        return ReplicationConnection, ReplicationCursor

    if driver == "aiosqlite":
        from aiosqlite import Connection, Cursor
        return Connection, Cursor
    if driver == "aiomysql":
        from aiomysql import Connection, Cursor
        return Connection, Cursor
    if driver == "asyncpg":
        from asyncpg import Connection
        from asyncpg.cursor import Cursor
        return Connection, Cursor
