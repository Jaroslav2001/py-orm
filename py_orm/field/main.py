from enum import Enum
from typing import (
    Any,
)

from pydantic.fields import FieldInfo as _FieldInfo, Undefined


class OnActions(str, Enum):
    CASCADE = 'CASCADE'
    SET_NULL = 'SET NULL'
    RESTRICT = 'RESTRICT'
    NO_ACTION = 'NO ACTION'
    SET_DEFAULT = 'SET DEFAULT'


class FieldInfo(_FieldInfo):
    __slots__ = _FieldInfo.__slots__ + (
        'length',

        'primary_key',
        'auto_increment',

        'foreign_key',
        'on_delete',
        'on_update',
        'many_key',

        'unique',
        'index',

        'nullable',
        'distinct',
        'query',
    )

    def __init__(self, default: Any = Undefined, **kwargs: Any):
        self.length = kwargs.pop('length', None)

        self.primary_key = kwargs.pop('primary_key', False)
        self.auto_increment = kwargs.pop('auto_increment', False)

        self.foreign_key = kwargs.pop('foreign_key', None)
        self.on_delete = kwargs.pop('on_delete', None)
        self.on_update = kwargs.pop('on_update', None)

        self.unique = kwargs.pop('unique', False)
        self.index = kwargs.pop('index', False)

        self.nullable = None
        self.distinct = kwargs.pop('distinct', False)
        self.query = kwargs.pop('query', None)

        super().__init__(default, **kwargs)
