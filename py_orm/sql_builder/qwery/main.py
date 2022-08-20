from abc import ABC
from typing import (
    Type,
    List,
    Generic,
    TypeVar,
    Set,
    Optional,
)

from error import NotLinkTableModel, BinaryOperationError
from py_orm import TBaseModel
from ..sql_builder import SQLBuilder
from ..t import T


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

    def __call__(self, *args, **kwargs) -> 'QwerySQL[TQwery[TBaseModel]]':
        return QwerySQL(self)

    def where(self, value: T) -> 'TQwery':
        if value.right is None:
            raise BinaryOperationError
        self._where = value
        return self

    def _get_where(self) -> str:
        if hasattr(self, '_where'):
            return f" WHERE {self._where.__sql__()}"
        return ''


TQwery = TypeVar('TQwery', bound=Qwery)


class QwerySQL(Generic[TQwery]):
    __sql__: str
    __qwery__: TQwery

    def __init__(self, __qwery: TQwery):
        self.__qwery__ = __qwery
        self.__sql__ = __qwery.__sql__()
