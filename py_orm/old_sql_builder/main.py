from typing import (
    TypeVar, Type, Iterator, Tuple, List,
)

from abc import ABC, abstractmethod

from py_orm import BaseModel, TBaseModel
from py_orm.dialect.main import dialect


class SQLBuilder(ABC):
    @abstractmethod
    def __sql__(self) -> str:
        ...

    @staticmethod
    def decorator_value(value) -> str:
        __types = dialect[BaseModel.__config_py_orm__.dialect].types.__types__
        return __types[type(value)].python_sql(value)

    @staticmethod
    def _join(values: str, parent: str):
        return f"{parent.join(values)}"

    @staticmethod
    def _build_py_orm_model(
            value: Type['TBaseModel'],
            data: List[tuple]
    ) -> Iterator['TBaseModel']:
        for column in data:
            virtual_data = {}
            for i, name in enumerate(value.__tabel_model__.__fields__.keys()):
                virtual_data[name] = column[i]
            yield value(**virtual_data)

    @staticmethod
    def _build_py_sql(*args, **kwargs) -> Tuple[tuple, dict]:
        __types = dialect[BaseModel.__config_py_orm__.dialect].types.__types__
        args = list(args)

        for i, j in enumerate(args):
            if j is None:
                args[i] = dialect[BaseModel.__config_py_orm__.dialect].null
            else:
                args[i] = __types[type(j)].python_sql(j)

        for i, j in kwargs.items():
            if j is None:
                kwargs[i] = dialect[BaseModel.__config_py_orm__.dialect].null
            else:
                kwargs[i] = __types[type(j)].python_sql(j)

        return tuple(args), kwargs


TSQLBuilder = TypeVar('TSQLBuilder', bound=SQLBuilder)
