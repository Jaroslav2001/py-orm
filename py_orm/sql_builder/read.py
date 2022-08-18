from typing import TYPE_CHECKING, Generic, TypeVar, Type, List, Iterator, Optional

from py_orm import TBaseModel
from .column import C
from .sql_builder import SQLBuilder


class Read(SQLBuilder, Generic[TBaseModel]):
    model: Type[TBaseModel]
    columns: List[str]
    value: TBaseModel
    _where: Optional[C]

    def __init__(
            self,
            model: Type[TBaseModel],
    ):
        self.model = model
        # add check BaseModel.__tabel_name__ is Error
        self._where = None
        self.columns = list(model.__fields__.keys())

    def where(self, value: C) -> 'Read':
        self._where = value
        return self

    def __str__(self):
        return f"SELECT {', '.join(self.columns)} " \
               f"FROM {self.model.__tabel_model__.__tabel_name__}" \
               f"{'' if self._where is None else ' '+str(self._where)};"
