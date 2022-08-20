from typing import Generic, Type

from py_orm import TBaseModel
from ..main import Qwery
from ...t.template import Template


class Create(Qwery, Generic[TBaseModel]):
    def __init__(
            self,
            value: Type[TBaseModel],
    ):
        super().__init__(value)

    def _values_t(self) -> str:
        return "{}"

    def _value_sql(self) -> str:
        return f"({(', '.join(Template(x).__sql__() for x in self.columns))})"

    def __sql__(self) -> str:
        return f"INSERT INTO {self.model.__tabel_model__.__tabel_name__} " \
               f"({', '.join(self.columns)}) VALUES " \
               f"{self._values_t()};"
