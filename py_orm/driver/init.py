from typing import (
    Literal,
    TypeAlias,
    List, Optional,
)

Driver: TypeAlias = Literal[
    "sqlite3", "pymysql", "psycopg2", "asyncpg", "aiomysql", "aiosqlite",
]
drivers: List[Driver] = [
    "sqlite3", "pymysql", "psycopg2", "asyncpg", "aiomysql", "aiosqlite",
]

SyncDriver: TypeAlias = Literal["sqlite3", "pymysql", "psycopg2"]
sync_drivers: List[SyncDriver] = ["sqlite3", "pymysql", "psycopg2"]

AsyncDriver: TypeAlias = Literal["asyncpg", "aiomysql", "aiosqlite"]
async_drivers: List[AsyncDriver] = ["asyncpg", "aiomysql", "aiosqlite"]


def is_async(driver: Driver) -> Optional[bool]:
    if driver in async_drivers:
        return False
    if driver in sync_drivers:
        return True
    return None
