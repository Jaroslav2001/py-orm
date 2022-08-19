from abc import ABC
from typing import Type, List, Generic, TypeVar

from error import NotLinkTableModel
from py_orm import TBaseModel
from .sql_builder import SQLBuilder


class Qwery(SQLBuilder, Generic[TBaseModel], ABC):
    model: Type[TBaseModel]
    columns: List[str]

    def __init__(
            self,
            model: Type[TBaseModel],
    ):
        if model.__tabel_model__ is None:
            raise NotLinkTableModel
        self.model = model
        self.columns = list(model.__fields__.keys())


TQwery = TypeVar('TQwery', bound=Qwery)
