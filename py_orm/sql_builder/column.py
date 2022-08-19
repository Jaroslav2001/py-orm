from typing import Optional

from .sql_builder import SQLBuilder
from py_orm import TBaseModel


class Column(SQLBuilder):
    column: str
    _table: TBaseModel

    def __init__(
            self,
            column: str,
            table: Optional[TBaseModel] = None,
    ):
        self.column = column
        self._table = table

    def _is_table(self) -> str:
        if self._table is None:
            return ''
        return f".{self._table.__tabel_model__.__tabel_name__}"

    def __sql__(self):
        return f"{self._is_table()}{self.column}"
