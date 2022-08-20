from typing import Generic

from py_orm import TBaseModel
from .main import Create


class CreateOne(Create, Generic[TBaseModel]):
    def _values_t(self) -> str:
        return self._value_sql()
