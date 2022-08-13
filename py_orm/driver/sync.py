from abc import ABC, abstractmethod
from typing import TypeVar

from error import NotSupportDriverError
from py_orm import BaseModel


class AbstractConnectionDriver(ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def cursor(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class AbstractCursorDriver(ABC):
    """PEP 249 - Python Database API Specification v2.0"""
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def execute(self, operation: str, *args, **kwargs):
        pass

    @abstractmethod
    def executemany(self, operation: str, *args, **kwargs):
        pass

    @abstractmethod
    def fetchone(self):
        pass

    @abstractmethod
    def fetchmany(self, size: int):
        pass

    @abstractmethod
    def fetchall(self):
        pass


def connect() -> 'TConnection':
    try:
        class Connection(
            BaseModel.config['driver'],
            AbstractConnectionDriver
        ):
            pass

        connection = Connection(
            *BaseModel.config['url'][0],
            **BaseModel.config['url'][1],
        )
    except NotImplementedError:
        raise NotSupportDriverError(type(BaseModel.config['driver']))
    else:
        return connection


TConnection = TypeVar('TConnection', bound=AbstractConnectionDriver)
