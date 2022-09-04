from typing import (
    TypeVar, Tuple,
)

from typing_extensions import (
    Type, Self,
)

from pydantic.fields import ModelField

from .crud import ModelMetaclassCRUD, BaseModelCRUD
from py_orm.field import TableField, FieldInfo


class ModelMetaclassDB(ModelMetaclassCRUD):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if not('__tabel_name__' in namespace):
            namespace['__tabel_name__'] = name

        _base_model: Type[TBaseModelDB] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        _base_model.__tabel_model__ = _base_model
        if _base_model.__module__ != __name__:

            if not hasattr(_base_model, '__table_field__'):
                _base_model.__table_field__ = TableField()

            for __name, __model in _base_model.__fields__.items():
                __model: ModelField
                if isinstance(__model.field_info, FieldInfo):
                    __field: FieldInfo = __model.field_info

                    if __field.primary_key:
                        _base_model.__table_field__.primary_key(__name)

                    if __field.auto_increment:
                        _base_model.__table_field__.auto_increment(__name)

                    if __field.unique:
                        _base_model.__table_field__.unique(__name)

                    if __field.index:
                        _base_model.__table_field__.index(__name)

            mcs.__py_orm__.add(_base_model)
        return _base_model

    def __getitem__(cls, item: str) -> Tuple[Self, ModelField]:
        if item in cls.__fields__:
            return cls, cls.__fields__[item]


class BaseModelDB(BaseModelCRUD, metaclass=ModelMetaclassDB):
    __tabel_name__: str
    __table_field__: TableField


TBaseModelDB = TypeVar('TBaseModelDB', bound=BaseModelDB)
