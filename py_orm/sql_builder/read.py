from typing import Generic

from py_orm import TBaseModel
from .qwery import Qwery


class Read(Qwery, Generic[TBaseModel]):
    def __sql__(self) -> str:
        return f"SELECT {', '.join(self.columns)} " \
               f"FROM {self.model.__tabel_model__.__tabel_name__}" \
               f"{self._get_where()};"
