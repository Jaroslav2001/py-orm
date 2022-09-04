from abc import ABC
from typing import (
    Generic,
)

from typing_extensions import (
    Type,
)

from ..terms import TableModel
from py_orm.models import TBaseModelDB


class ModelBuilder(Generic[TBaseModelDB], ABC):
    _model: Type[TBaseModelDB]
    _name: TableModel[TBaseModelDB]

    def __init__(self, model: Type[TBaseModelDB]):
        self._model = model
        self._name = TableModel(model)

    @property
    def __sql__(self) -> str:
        return f"CREATE TABLE {self._name}"

    def __eq__(self, other):
        return f"ALERT TABLE {self._name}"
