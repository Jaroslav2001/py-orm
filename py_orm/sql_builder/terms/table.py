from typing import Type, Iterable, Generic

from pydantic.fields import ModelField

from py_orm.error import ColumnError
from py_orm.field import FieldInfo
from py_orm.models import TBaseModelCRUD


from .node import Column
from .sql import SQL


class TableModel(Generic[TBaseModelCRUD], SQL):
    _value: Type[TBaseModelCRUD]

    def __init__(self, __value: Type[TBaseModelCRUD]):
        self._value = __value

    def column(self, __name: str) -> Column:
        if __name in self._value.__fields__.keys():
            __field = self._value.__fields__[__name]
            __field: ModelField
            if isinstance(__field.field_info, FieldInfo):
                __field: FieldInfo = __field.field_info
                return Column(
                    __name,
                    self._value,
                    alias=__field.alias,
                    distinct=__field.distinct,
                )
            return Column(
                __name,
                self._value,
                alias=__field.field_info.alias,
            )
        raise ColumnError()

    def column_all(self) -> Iterable[Column]:
        for __name, __model in self._value.__fields__.items():
            __model: ModelField
            if isinstance(__model.field_info, FieldInfo):
                __field: FieldInfo = __model.field_info
                yield Column(
                    __name,
                    self._value,
                    alias=__field.alias,
                    distinct=__field.distinct,
                )
            else:
                yield Column(
                    __name,
                    self._value,
                    alias=__model.field_info.alias,
                )

    def column_key_model(self) -> Iterable[Column]:
        for __key in self._value.__tabel_model__.__table_field__.primary_key_:
            yield Column(
                __key,
                self._value,
            )

    @property
    def __sql__(self) -> str:
        return f'"{self._value.__tabel_model__.__tabel_name__}"'
