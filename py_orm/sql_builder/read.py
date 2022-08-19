from typing import Generic

from py_orm import TBaseModel
from .template import T
from .qwery import Qwery


class Read(Qwery, Generic[TBaseModel]):
    value: TBaseModel
    _where: T

    def where(self, value: T) -> 'Read':
        self._where = value
        return self

    def _get_where(self) -> str:
        if hasattr(self, '_where'):
            return f" {self._where()}"
        return ''

    def __sql__(self) -> str:
        return f"SELECT {', '.join(self.columns)} " \
               f"FROM {self.model.__tabel_model__.__tabel_name__}" \
               f"{self._get_where()};"
