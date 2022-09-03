from abc import ABC
from typing import (
    Generic,
    TypeVar,
    Tuple,
    Set,
)

from typing_extensions import (
    Self,
    Type,
)

from pydantic.fields import ModelField

from ..terms import TableModel
from ..field import FieldInfo
from .main import ModelMetaclass, BaseModel


class ModelMetaclassDB(ModelMetaclass):
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
        if _base_model.__module__ != __name__:
            if hasattr(_base_model, '__query__'):
                _base_model.__query__ = \
                    ModelBuilder(_base_model).extend(_base_model.__query__)
            else:
                _base_model.__query__ = ModelBuilder(_base_model)

            for __name, __model_field in _base_model.__fields__.items():
                __name: str
                __model_field: ModelField
                if isinstance(__model_field.field_info, FieldInfo):
                    __field_info: FieldInfo = __model_field.field_info

                    if __field_info.primary_key:
                        _base_model.__query__.primary_key(__name)
                    if __field_info.auto_increment:
                        _base_model.__query__.auto_increment(__name)

                    if __field_info.index:
                        _base_model.__query__.index(__name)
                    if __field_info.unique:
                        _base_model.__query__.unique(__name)

            mcs.__py_orm__.add(_base_model)
        return _base_model

    def __getitem__(cls, item: str) -> Tuple[Self, ModelField]:
        if item in cls.__fields__:
            return cls, cls.__fields__[item]


class BaseModelDB(BaseModel, metaclass=ModelMetaclassDB):
    __tabel_name__: str
    __query__: 'AbstractModelBuilder'


TBaseModelDB = TypeVar('TBaseModelDB', bound=BaseModelDB)


class AbstractModelBuilder(ABC):
    _primary_key: Set[str]
    _auto_increment: Set[str]

    _unique: Set[str]
    _index: Set[str]

    def __init__(self):
        self._primary_key = set()
        self._auto_increment = set()
        self._unique = set()
        self._index = set()

    def extend(self, builder: 'AbstractModelBuilder') -> Self:
        self._primary_key.union(builder._primary_key)
        self._auto_increment.union(builder._auto_increment)
        self._unique.union(builder._unique)
        self._index.union(builder._index)
        return self

    def primary_key(self, *args: str) -> Self:
        self._primary_key.union(args)
        return self

    def auto_increment(self, *args: str) -> Self:
        self._auto_increment.union(args)
        return self

    def unique(self, *args: str) -> Self:
        self._unique.union(args)
        return self

    def index(self, *args: str) -> Self:
        self._index.union(args)
        return self


class ModelBuilder(Generic[TBaseModelDB], AbstractModelBuilder, ABC):
    _model: Type[TBaseModelDB]
    _name: TableModel[TBaseModelDB]

    def __init__(self, model: Type[TBaseModelDB]):
        super().__init__()
        self._model = model
        self._name = TableModel(model)

    @property
    def __sql__(self) -> str:
        return f"CREATE TABLE {self._name}"

    def __eq__(self, other):
        return f"ALERT TABLE {self._name}"
