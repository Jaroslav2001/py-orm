from typing import TypeVar

from abc import ABC, abstractmethod

from py_orm import BaseModel
from py_orm.dialect.main import dialect


class SQLBuilder(ABC):
    @staticmethod
    def decorator_value(value):
        __types = dialect[BaseModel.__config_py_orm__.dialect].types.__types__
        return __types[type(value)].python_sql(value)

    @abstractmethod
    def __sql__(self) -> str:
        ...

    def __call__(self, *args, **kwargs) -> str:
        return self.__sql__()


TSQLBuilder = TypeVar('TSQLBuilder', bound=SQLBuilder)
