from typing import List, Optional

from py_orm import BaseModel

from ..sql_builder import SQLBuilder
from dialect import dialect, DialectSQL
from .column import Column


class MigrationsModel(SQLBuilder):
    name: str
    columns: List[Column]
    mode: Optional[bool]

    def __init__(
            self,
            name: str,
            columns: List[Column],
            mode: Optional[bool] = None,
    ):
        self.name = name
        self.columns = columns
        self.mode = mode

    @staticmethod
    def _dialect() -> DialectSQL:
        return dialect[BaseModel.__config_py_orm__.dialect]

    def __sql_create_table__(self) -> str:
        _columns = ",\n\t".join((x.__sql__() for x in self.columns))
        return f"{self._dialect().create_table} {self.name} (\n\t{_columns}\n);"

    def __sql_drop_table__(self) -> str:
        return f"{self._dialect().drop_table} {self.name};"

    def __sql_alert__table(self) -> str:
        # create analise
        return f""

    def __sql__(self) -> str:
        if isinstance(self.mode, bool):
            if self.mode:
                return self.__sql_create_table__()
            return self.__sql_drop_table__()
        return self.__sql_alert__table()
