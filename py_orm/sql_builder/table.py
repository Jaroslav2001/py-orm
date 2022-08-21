from typing import Type, Iterable, Union

from pydantic.fields import ModelField
from pypika import Table as _Table
from pypika import Field as _Field

from py_orm import TBaseModel
from py_orm.field import FieldInfo


class TableModel(_Table):
    __value: Type[TBaseModel]

    def __init__(self, name: Type[TBaseModel]):
        self.__value = name
        super().__init__(name.__tabel_model__.__tabel_name__)

    def column_all(self) -> Iterable[_Field]:
        return map(_Field, self.__value.__fields__.keys())

    def column_key_model(self) -> Iterable[_Field]:
        for __name, __model in self.__value.__tabel_model__.__fields__.items():
            __model: ModelField
            if isinstance(__model.field_info, FieldInfo):
                if __model.field_info.primary_key:
                    yield __name


