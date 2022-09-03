from typing import (
    Optional,
    List,
    Generic,
    TypeVar,
    Callable
)


from typing_extensions import (
    Type,
    Self,
    TYPE_CHECKING,
)


from ..terms import *
from .main import BaseModel, ModelMetaclass

if TYPE_CHECKING:
    from .query_builder_model import TBaseModelDB


# CRUD Model
class ModelMetaclassCRUD(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[TBaseModelCRUD] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        if _base_model.__module__ != __name__:
            _base_model.__query__ = QueryBuilder(_base_model)
        return _base_model


class BaseModelCRUD(BaseModel, metaclass=ModelMetaclassCRUD):
    __tabel_model__: Optional['TBaseModelDB']
    __query__: 'QueryBuilder'


TBaseModelCRUD = TypeVar('TBaseModelCRUD', bound=BaseModelCRUD)


# Create Model
class ModelMetaclassCreate(ModelMetaclassCRUD):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[BaseModelCreate] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        if _base_model.__module__ != __name__:
            _base_model.__query__ = _base_model.__query__.insert_into()
        return _base_model


class BaseModelCreate(BaseModelCRUD, metaclass=ModelMetaclassCreate):
    __tabel_name__: str
    __query__: 'QueryBuilder'


TBaseModelCreate = TypeVar('TBaseModelCreate', bound=BaseModelCreate)


# Read Model
class ModelMetaclassRead(ModelMetaclassCRUD):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[BaseModelRead] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        if _base_model.__module__ != __name__:
            _base_model.__query__ = _base_model.__query__.select()
        return _base_model


class BaseModelRead(BaseModelCRUD, metaclass=ModelMetaclassRead):
    __tabel_name__: str
    __query__: 'QueryBuilder'


TBaseModelRead = TypeVar('TBaseModelRead', bound=BaseModelRead)


# Update Model
class ModelMetaclassUpdate(ModelMetaclassCRUD):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[BaseModelUpdate] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        if _base_model.__module__ != __name__:
            _base_model.__query__ = _base_model.__query__.update()
        return _base_model


class BaseModelUpdate(BaseModelCRUD, metaclass=ModelMetaclassUpdate):
    __tabel_name__: str
    __query__: 'QueryBuilder'


TBaseModelUpdate = TypeVar('TBaseModelUpdate', bound=BaseModelUpdate)


# Delete Model
class ModelMetaclassDelete(ModelMetaclassCRUD):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[BaseModelDelete] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        if _base_model.__module__ != __name__:
            _base_model.__query__ = _base_model.__query__.delete()
        return _base_model


class BaseModelDelete(BaseModelCRUD, metaclass=ModelMetaclassDelete):
    __tabel_name__: str
    __query__: 'QueryBuilder'


TBaseModelDelete = TypeVar('TBaseModelDelete', bound=BaseModelDelete)


class QueryBuilder(Generic[TBaseModelCRUD], SQL):
    _select: bool
    _insert_into: bool
    _update: bool
    _delete: bool

    _t_base_model: Optional[Type[TBaseModelCRUD]]

    _columns: List[Column]
    _values: List[TBaseModelCRUD]
    _set:  List[Column]
    _where: List[TNode]

    def __init__(self, t_base_model: Type[TBaseModelCRUD]):
        self._t_base_model = t_base_model

        self._insert_into = False
        self._select = False
        self._update = False
        self._delete = False

        self._columns = list(TableModel(self._t_base_model).column_all())
        self._values = []
        self._set = []
        self._where = []

    # CRUD Operation

    def insert_into(self) -> Self:
        self._insert_into = True
        self._select = False
        self._update = False
        self._delete = False
        return self

    def select(self) -> Self:
        self._insert_into = False
        self._select = True
        self._update = False
        self._delete = False
        return self

    def update(self) -> Self:
        self._insert_into = False
        self._select = False
        self._update = True
        self._delete = False
        return self

    def delete(self) -> Self:
        self._insert_into = False
        self._select = False
        self._update = False
        self._delete = True
        return self

    # Value Operation

    def values(self, *args: TBaseModelCRUD) -> Self:
        self._values.extend(args)
        return self

    # Operation where

    def where(self, *args: TNode) -> Self:
        if args:
            self._where.extend(args)
        elif not self._where:
            self._where.extend(map(
                lambda x: x == Parameter(x.column),
                TableModel(self._t_base_model).column_key_model(),
            ))
        return self

    # Operator set

    def set(self, *args: TNode) -> Self:
        self._set.extend(args)
        return self

    def limit(self) -> Self:
        return self

    def offset(self) -> Self:
        return self

    # Operator order_by

    def order_by(self) -> Self:
        return self

    def group_by(self) -> Self:
        return self

    def having(self) -> Self:
        return self

    @property
    def __sql__(self) -> str:
        __table = TableModel(self._t_base_model)

        if self._insert_into:
            return f"INSERT INTO " \
                   f"{__table} ({self.__sql__columns}) " \
                   f"VALUES {self.__sql__values}"

        if self._select:
            return f"SELECT {self.__sql__columns} " \
                   f"FROM {__table}" \
                   f"{self.__sql__where}"

        if self._update:
            return f"UPDATE {__table} " \
                   f"SET {self.__sql__set}" \
                   f"{self.__sql__where}"

        if self._delete:
            return f"DELETE FROM {__table}" \
                   f"{self.__sql__where}"

    @property
    def __sql__columns(self) -> str:
        return ', '.join(map(lambda x: x.__sql__, self._columns))

    @property
    def __sql__values(self) -> str:
        if self._values:
            return ", ".join(map(lambda x: x.__sql__, self._values))
        return ParameterFor(self._t_base_model).__sql__

    @property
    def __sql__set(self) -> str:
        if self._set:
            return ", ".join(map(lambda x: x == Parameter(x.column), self._set))
        return ", ".join(map(
            lambda x: (x == Parameter(x.column)).__sql__,
            TableModel(self._t_base_model).column_all(),
        ))

    @property
    def __sql__where(self) -> str:
        if self._where:
            if len(self._where) == 1:
                return f" WHERE {self._where[0].__sql__}"
            return f" WHERE {'AND'.join(self._where)}"
        return ''


def builder_manager(
        func: Callable[..., QueryBuilder],
        return_model: Optional[TBaseModelRead] = None,
):
    def wrapper(cls, *args, **kwargs):
        __sql__: str = func(cls, *args, **kwargs).__sql__

        def decorator():
            return
        return decorator
    return wrapper
