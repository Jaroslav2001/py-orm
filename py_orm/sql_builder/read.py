from typing import TYPE_CHECKING, Generic, TypeVar, Type, List, Iterator

from py_orm import BaseModel
from .sql_builder import SQLBuilder

TModel = TypeVar('TModel', bound=BaseModel)
TSchema = TypeVar('TSchema', bound=BaseModel)


class Read(SQLBuilder, Generic[TModel, TSchema]):
    db_model: Type[TModel]
    schema_model: Type[TSchema]
    columns: List[str]
    value: TSchema

    def __init__(
            self,
            db_model: Type[TModel],
            schema_model: Type[TSchema],
    ):
        self.db_model = db_model
        # add check insert_into.__tabel_name__ is Error
        self.schema_model = schema_model
        self.columns = list(schema_model.__fields__.keys())

    def where(self, value) -> 'Read':
        ...

    def __str__(self):
        return f"SELECT {', '.join(self.columns)} " \
               f"FROM {self.db_model.__tabel_name__};"
