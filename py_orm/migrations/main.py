from typing import TYPE_CHECKING, List

from pydantic.fields import ModelField

from py_orm import BaseModel
from py_orm.main import is_type
from py_orm.field import FieldInfo
from py_orm.dialect import dialect

from .attribute import Attribute
from .column import Column
from .migrations_model import MigrationsModel

if TYPE_CHECKING:
    from py_orm.main import TBaseModel


def migrations():
    new_model: List[MigrationsModel] = []
    old_model: List[MigrationsModel] = []

    for model in BaseModel.__py_orm__:
        model: TBaseModel
        migration_model: MigrationsModel = MigrationsModel(
            name=model.__tabel_name__,
            columns=[]
        )
        for column in model.fields:
            column: ModelField

            # type check - is_type() is None and type
            type_ = None
            is_null = is_type(column.type_, 'Optional')
            if is_null[0]:
                for i in is_null[1]:
                    if not(i is None):
                        type_ = i
            elif len(is_null[1]) == 0:
                type_ = is_null[2]

            # get sql type
            field_info: FieldInfo = column.field_info
            sql_type: str = ''

            for i in dialect[BaseModel.__config_py_orm__['dialect']]['types']:
                sql_type = i.type_python_to_sql(
                    value=type_,
                    length=field_info.length,
                )
                if isinstance(sql_type, str):
                    break
            sql_type: str

            migration_model.columns.append(Column(
                name=column.name,
                type_=sql_type,
                length=field_info.length,
                attribute=Attribute(
                    primary_key=field_info.primary_key,
                    foreign_key=field_info.foreign_key,
                    unique=field_info.unique,
                    index=field_info.index,
                    auto_increment=field_info.auto_increment,
                    null=is_null[0],
                ),
            ))
        new_model.append(
            migration_model
        )

    # Old models
