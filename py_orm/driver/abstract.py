from abc import ABC, abstractmethod
from typing import TypeVar, AsyncIterator


class AbstractCursor(ABC):
    @abstractmethod
    async def execute(self, sql: str) -> 'TAbstractCursor':
        ...

    @abstractmethod
    async def executemany(self, sql: str) -> 'TAbstractCursor':
        ...

    @abstractmethod
    async def fetchone(self):
        ...

    @abstractmethod
    async def fetchmany(self, size: int = None):
        ...

    @abstractmethod
    async def fetchall(self):
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    def __aiter__(self) -> AsyncIterator:
        ...


class AbstractConnector(ABC):
    @abstractmethod
    async def cursor(self) -> 'TAbstractCursor':
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __await__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...


TAbstractCursor = TypeVar('TAbstractCursor', bound=AbstractCursor)
TAbstractConnector = TypeVar('TAbstractConnector', bound=AbstractConnector)
