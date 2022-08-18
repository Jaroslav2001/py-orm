from typing import Generic, Type, List, Iterator

from py_orm import TBaseModel
from .sql_builder import SQLBuilder


class Create(SQLBuilder, Generic[TBaseModel]):
    model: Type[TBaseModel]
    columns: List[str]
    value: TBaseModel

    def __init__(
            self,
            model: Type[TBaseModel],
    ):
        self.model = model
        # add check BaseModel.__tabel_name__ is Error
        self.columns = list(model.__fields__.keys())

    def _value(self, value: TBaseModel) -> str:
        return f"({', '.join(self.decorator_value(getattr(value, x)) for x in self.columns)})"

    def value(self, value: TBaseModel) -> str:
        return f"INSERT INTO {self.model.__tabel_model__.__tabel_name__} "\
            f"({', '.join(self.columns)}) VALUES "\
            f"{self._value(value)};"

    def values(self, values: Iterator[TBaseModel]) -> str:
        return f"INSERT INTO {self.model.__tabel_model__.__tabel_name__} " \
            f"({', '.join(self.columns)}) VALUES " \
            f"{', '.join(self._value(x) for x in values)};"
