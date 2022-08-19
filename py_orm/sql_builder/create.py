from typing import Generic, List, Iterator, Type

from py_orm import TBaseModel
from .qwery import Qwery


class Create(Qwery, Generic[TBaseModel]):
    values: List[TBaseModel]

    def __init__(
            self,
            value: Type[TBaseModel],
    ):
        self.values = []
        super().__init__(value)

    def _value_sql(self, value: TBaseModel) -> str:
        return f"({', '.join(self.decorator_value(getattr(value, x)) for x in self.columns)})"

    def __value__(self, value: TBaseModel) -> 'Create':
        self.values.append(value)
        return self

    def __values__(self, values: Iterator[TBaseModel]) -> 'Create':
        self.values.extend(values)
        return self

    def __sql__(self) -> str:
        return f"INSERT INTO {self.model.__tabel_model__.__tabel_name__} " \
               f"({', '.join(self.columns)}) VALUES " \
               f"{', '.join(self._value_sql(x) for x in self.values)};"
