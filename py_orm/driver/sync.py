from abc import ABC, abstractmethod
from typing import TypeVar, Type

from error import NotSupportDriverError
from py_orm import BaseModel


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
    def __enter__(self):
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
    def execute(self, operation: str, *args, **kwargs):
        ...

    @abstractmethod
    def executemany(self, operation: str, *args, **kwargs):
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


def connect() -> 'TConnection':
    try:
        class Cursor(
            BaseModel.__config_py_orm__['driver'][1],
            AbstractCursorDriver
        ):
            pass

        class Connection(
            BaseModel.__config_py_orm__['driver'][0],
            AbstractConnectionDriver
        ):
            def cursor(self, factory=Cursor) -> 'TCursor':
                return super().cursor(factory=factory)

        connection = Connection(
            *BaseModel.__config_py_orm__['connect'][0],
            **BaseModel.__config_py_orm__['connect'][1],
        )
    except NotImplementedError:
        raise NotSupportDriverError(type(BaseModel.__config_py_orm__['driver']))
    else:
        return connection


TConnection = TypeVar('TConnection', bound=AbstractConnectionDriver)
TCursor = TypeVar('TCursor', bound=AbstractCursorDriver)
