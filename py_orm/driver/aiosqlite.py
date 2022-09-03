import sqlite3
from aiosqlite import (
    Connection as _Connection,
    Cursor as _Cursor
)


from .abstract import (
    AbstractCursor,
    AbstractConnector,
    TAbstractCursor,
    TAbstractConnector,
)

from py_orm import BaseModel


class Cursor(_Cursor, AbstractCursor):
    pass


class Connection(_Connection, AbstractConnector):
    def __init__(self):
        def connector() -> sqlite3.Connection:
            return sqlite3.connect(
                BaseModel.__config_py_orm__.database
            )
        super().__init__(connector, 64)

    async def cursor(self) -> Cursor:
        return Cursor(self, await self._execute(self._conn.cursor))
