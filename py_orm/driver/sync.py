from abc import ABC, abstractmethod


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
