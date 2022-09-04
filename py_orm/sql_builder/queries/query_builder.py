import re
from typing import (
    Optional,
    List,
    Generic,
)


from typing_extensions import (
    Type,
    Self,
)


from ..terms import *
from py_orm.models import TBaseModelCRUD


class Request:
    __sql__: str

    def __init__(self, __query: 'QueryBuilder'):
        self.__sql__ = __query.__sql__

    def __call__(self, *args, **kwargs) -> str:
        regex_ = re.search(
            r'\$for\(([\w\s\{\}\.,]*)\)',
            self.__sql__,
        )
        if regex_ is None:
            return self.__sql__.format(*args, **kwargs)
        __result: List[str] = []
        for _model in args:
            __result.append(regex_.groups()[0].format(**_model))
        return re.sub(
            r'\$for\(([\w\s\{\}\.,]*)\)',
            ', '.join(__result),
            self.__sql__,
        )


class QueryBuilder(Generic[TBaseModelCRUD], SQL):
    _select: bool
    _insert_into: bool
    _update: bool
    _delete: bool

    _t_base_model: Type[TBaseModelCRUD]

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
