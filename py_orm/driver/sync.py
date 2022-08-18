from abc import ABC, abstractmethod
from typing import TypeVar, Type, TYPE_CHECKING, Iterator, List

from error import NotSupportDriverError
from py_orm import BaseModel, TBaseModel

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
    def cursor(self, factory: Type['TCursor'] = 'TCursor') -> 'TCursor':
        ...

    @abstractmethod
    def __enter__(self) -> 'TCursor':
        ...

    @abstractmethod
    def __exit__(self):
        ...

    @abstractmethod
    def __init__(self, *args, **kwargs):
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


class Cursor(
    BaseModel.__config_py_orm__['driver'][1],
    AbstractCursorDriver
):
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


class Connection(
    BaseModel.__config_py_orm__['driver'][0],
    AbstractConnectionDriver
):
    def cursor(self, factory=Cursor) -> 'TCursor':
        return super().cursor(factory=factory)


def connect() -> 'TConnection':
    try:
        connection = Connection(
            *BaseModel.__config_py_orm__['connect'][0],
            **BaseModel.__config_py_orm__['connect'][1],
        )
    except NotImplementedError:
        raise NotSupportDriverError(type(BaseModel.__config_py_orm__['driver']))
    else:
        return connection


TConnection = TypeVar('TConnection', bound=Connection)
TCursor = TypeVar('TCursor', bound=Cursor)
