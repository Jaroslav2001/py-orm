from typing import (
    Type,
)

from pypika import (
    Query as _Query,
    Field as _Field,
    Criterion as _Criterion,
)
from pypika.queries import QueryBuilder

from py_orm import TBaseModel

from .parameter import p, p_dict
from .table import TableModel


class Query(_Query):
    @classmethod
    def read(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        """SELECT *columns FROM table;"""
        return cls.select(
            *TableModel(__value).column_all()
        ).from_(
            TableModel(__value)
        )

    @classmethod
    def read_one(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        """SELECT *columns FROM table WHERE id={};"""
        return cls.read(__value).where(
            _Criterion.all(
                __columns == p()
                for __columns in TableModel(__value).column_key_model()
            )
        )

    @classmethod
    def read_many(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls.read(__value).limit(p()).offset(p())

    @classmethod
    def _create(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls.into(
            TableModel(__value)
        ).columns(
            *TableModel(__value).column_all()
        )

    @classmethod
    def create(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls._create(__value).insert(p_dict(
            __value.__fields__.keys()
        ))

    @classmethod
    def renames(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls.update(
            TableModel(__value)
        )

    @classmethod
    def rename(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        __cls = cls.renames(__value)
        for item in TableModel(__value).column_all():
            __cls = __cls.set(
                item, p(item.name)
            )
        return __cls.where(
            _Criterion.all(
                __columns == p()
                for __columns in TableModel(__value).column_key_model()
            )
        )

    @classmethod
    def delete_all(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls.from_(
            TableModel(__value)
        ).delete()

    @classmethod
    def delete(cls, __value: Type[TBaseModel]) -> "QueryBuilder":
        return cls.from_(
            TableModel(__value)
        ).where(
            _Criterion.all(
                __columns == p()
                for __columns in TableModel(__value).column_key_model()
            )
        ).delete()
