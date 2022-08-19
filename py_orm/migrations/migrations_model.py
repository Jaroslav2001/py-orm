from typing import List

from pydantic import BaseModel as _BaseModel

from py_orm import BaseModel
from dialect import dialect, DialectSQL
from .column import Column


class MigrationsModel(_BaseModel):
    name: str
    columns: List[Column]

    @staticmethod
    def __get_dialect__() -> DialectSQL:
        return dialect[BaseModel.__config_py_orm__.dialect]

    def __sql_create_table__(self) -> str:
        _dialect = self.__get_dialect__()
        _columns = ",\n\t".join((x.__sql__() for x in self.columns))
        return f"{_dialect.create_table} {self.name} (\n\t{_columns}\n);"

    def __sql_drop_table__(self) -> str:
        _dialect = self.__get_dialect__()
        return f"{_dialect.drop_table} {self.name};"
