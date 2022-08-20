from typing import List, Iterator, Generic

from pydantic.fields import ModelField

from py_orm.field import FieldInfo
from py_orm import TBaseModel, T, add_
from sql_builder.qwery import Qwery


class Update(Qwery, Generic[TBaseModel]):
    _set: List[T] = []

    def auto_set(self) -> 'Update':
        for column in self.columns:
            self._set.append(T(c=column) == T(column))

        # model update where primary key
        __primary_columns: List[str] = []
        for _i, _k in self.model.__fields__.items():
            _k: ModelField
            if isinstance(_k.field_info, FieldInfo):
                if _k.field_info.primary_key:
                    __primary_columns.append(_i)

        __result = T(c=__primary_columns.pop(0)) == T()
        while len(__primary_columns) != 0:
            __result = add_(__result, T(c=__primary_columns.pop(0)) == T())
        self.where(__result)
        return self

    def set(self, *args: T) -> 'Update':
        self._set.extend(args)
        return self

    def __sql__(self) -> str:
        return f"UPDATE {self.model.__tabel_model__.__tabel_name__} " \
               f"SET {', '.join(self._set_sql())}" \
               f"{self._get_where()};"

    def _set_sql(self) -> Iterator[str]:
        for __value in self._set:
            yield __value.__sql__()
