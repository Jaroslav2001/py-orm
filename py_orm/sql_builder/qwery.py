from abc import ABC
from typing import Type, List, Generic, TypeVar

from error import NotLinkTableModel, BinaryOperationError
from py_orm import TBaseModel
from .sql_builder import SQLBuilder
from .t import T


class Qwery(SQLBuilder, Generic[TBaseModel], ABC):
    model: Type[TBaseModel]
    columns: List[str]
    _where: T

    def __init__(
            self,
            model: Type[TBaseModel],
    ):
        if model.__tabel_model__ is None:
            raise NotLinkTableModel
        self.model = model
        self.columns = list(model.__fields__.keys())

    def where(self, value: T) -> 'TQwery':
        if value.right is None:
            raise BinaryOperationError
        self._where = value
        return self

    def _get_where(self) -> str:
        if hasattr(self, '_where'):
            return f" WHERE {self._where()}"
        return ''


TQwery = TypeVar('TQwery', bound=Qwery)
