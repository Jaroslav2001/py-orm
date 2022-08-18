from abc import ABC, abstractmethod
from typing import TypeVar, TYPE_CHECKING, Iterator, List

from error import NotSupportDriverError
from py_orm import BaseModel, TBaseModel
from dialect.main import default_driver


if TYPE_CHECKING:
    from py_orm import Read


class AbstractConnectionDriver(ABC):
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


class AbstractCursorDriver(ABC):
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

    def get_all(self, value: 'Read[TBaseModel]') -> Iterator[TBaseModel]:
        self.execute(str(value))
        return self._build_py_orm_model(value=value, data=self.fetchall())


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
