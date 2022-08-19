from abc import ABC, abstractmethod
from typing import TypeVar, Iterator

from error import NotSupportDriverError
from py_orm import BaseModel, TBaseModel, Read
from dialect.main import default_driver
from sql_builder import Create
from .base import BaseConnectionDriver, BaseCursorDriver


class AbstractConnectionDriver(BaseConnectionDriver, ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...

    @abstractmethod
    def cursor(self, *args, **kwargs) -> 'TCursor':
        ...

    @abstractmethod
    def __enter__(self) -> 'TCursor':
        ...

    @abstractmethod
    def __exit__(self):
        ...


class AbstractCursorDriver(BaseCursorDriver, ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    connection: 'TConnection'

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def execute(self, sql: str, *args, **kwargs):
        ...

    @abstractmethod
    def executemany(self, sql: str, *args, **kwargs):
        ...

    @abstractmethod
    def fetchone(self):
        ...

    @abstractmethod
    def fetchmany(self, size: int):
        ...

    @abstractmethod
    def fetchall(self):
        ...

    def create(self, __qwery: Create, __value: TBaseModel, *args: TBaseModel):
        self.execute(__qwery.__value__(__value).__values__(args).__sql__())

    def read_all(self, __qwery: Read, *args, **kwargs) -> Iterator[TBaseModel]:
        args, kwargs = self._build_py_sql(*args, **kwargs)
        self.execute(__qwery.__sql__().format(*args, **kwargs))
        return self._build_py_orm_model(value=__qwery.model, data=self.fetchall())


if BaseModel.__config_py_orm__.driver is None:
    BaseModel.__config_py_orm__.driver = default_driver[(
        BaseModel.__config_py_orm__.dialect,
        False,
    )]
    BaseModel.__config_py_orm__.async_ = False

# ========================== sqlite3 ===============================================


if 'sqlite3' == BaseModel.__config_py_orm__.driver:
    from sqlite3 import (
        Connection as _Connection,
        Cursor as _Cursor,
    )

    class Cursor(_Cursor, AbstractCursorDriver):
        pass


    class Connection(_Connection, AbstractConnectionDriver):
        def cursor(self, **kwargs) -> 'TCursor':
            return super().cursor(factory=Cursor)


# ========================== NotSupportDriverError ===============================================
else:
    raise NotSupportDriverError


def connect() -> 'TConnection':
    if 'sqlite3' == BaseModel.__config_py_orm__.driver:
        return Connection(BaseModel.__config_py_orm__.database)
    else:
        raise NotSupportDriverError


TConnection = TypeVar('TConnection', bound=Connection)
TCursor = TypeVar('TCursor', bound=Cursor)
