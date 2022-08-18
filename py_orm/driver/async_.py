from abc import ABC, abstractmethod
from typing import (
    TypeVar,
    TYPE_CHECKING,
    NoReturn,
    List,
    Iterator,
)

from dialect.main import default_driver
from error import NotSupportDriverError
from py_orm import BaseModel, TBaseModel

if TYPE_CHECKING:
    from py_orm import Read


class AbstractConnectionDriver(ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    @abstractmethod
    async def close(self) -> NoReturn:
        ...

    @abstractmethod
    async def commit(self) -> NoReturn:
        ...

    @abstractmethod
    async def rollback(self) -> NoReturn:
        ...

    @abstractmethod
    async def cursor(
            self,
            *args,
            **kwargs,
    ) -> 'TCursor':
        ...

    @abstractmethod
    async def __aenter__(self) -> 'TCursor':
        ...

    @abstractmethod
    async def __aexit__(self) -> NoReturn:
        ...


class AbstractCursorDriver(ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    connection: 'TConnection'

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def execute(self, sql: str, *args, **kwargs):
        ...

    @abstractmethod
    async def executemany(self, sql: str, *args, **kwargs):
        ...

    @abstractmethod
    async def fetchone(self):
        ...

    @abstractmethod
    async def fetchmany(self, size: int):
        ...

    @abstractmethod
    async def fetchall(self):
        ...

    @staticmethod
    def _build_py_orm_model(
            value: 'Read[TBaseModel]',
            data: List[tuple]
    ) -> Iterator['TBaseModel']:
        for column in data:
            virtual_data = {}
            for i, name in enumerate(value.columns):
                virtual_data[name] = column[i]
            yield value.model(**virtual_data)

    async def get_all(self, value: 'Read[TBaseModel]') -> Iterator['TBaseModel']:
        await self.execute(str(value))
        return self._build_py_orm_model(value=value, data=await self.fetchall())


if BaseModel.__config_py_orm__.driver is None:
    BaseModel.__config_py_orm__.driver = default_driver[(
        BaseModel.__config_py_orm__.dialect,
        True,
    )]
    BaseModel.__config_py_orm__.async_ = True


# ========================== aiosqlite ===============================================


if 'aiosqlite' == BaseModel.__config_py_orm__.driver:
    from aiosqlite import (
        Connection as _Connection,
        Cursor as _Cursor,
    )

    class Cursor(_Cursor, AbstractCursorDriver):
        pass


    class Connection(_Connection, AbstractConnectionDriver):
        async def cursor(self, **kwargs) -> 'TCursor':
            return Cursor(self, await self._execute(self._conn.cursor))


# ========================== NotSupportDriverError ===============================================
else:
    raise NotSupportDriverError


def connect() -> 'TConnection':
    if 'aiosqlite' == BaseModel.__config_py_orm__.driver:
        import sqlite3

        def _connector() -> sqlite3.Connection:
            loc = BaseModel.__config_py_orm__.database
            return sqlite3.connect(loc)

        return Connection(
            _connector,
            iter_chunk_size=64
        )
    else:
        raise NotSupportDriverError


TConnection = TypeVar('TConnection', bound=Connection)
TCursor = TypeVar('TCursor', bound=Cursor)
