from typing import TYPE_CHECKING, List, Optional, NoReturn

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


def execute(sql: str, *args, **kwargs) -> NoReturn:
    if BaseModel.__config_py_orm__.async_:
        # Create execute async_
        pass
    else:
        from py_orm.driver.sync import connect, TConnection

        with connect() as connect_:
            connect_: TConnection
            cursor = connect_.cursor()
            cursor.execute(sql, *args, **kwargs)
            connect_.commit()


def get_new_model() -> List[MigrationsModel]:
    new_model: List[MigrationsModel] = []
    for model in BaseModel.__py_orm__:
        model: TBaseModel
        migration_model: MigrationsModel = MigrationsModel(
            name=model.__tabel_name__,
            columns=[]
        )
        for column in model.__fields__.values():
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

            for i in dialect[BaseModel.__config_py_orm__.dialect].__types__().values():
                sql_type = i.type_python_to_sql(
                    value=type_,
                    length=field_info.length if isinstance(field_info, FieldInfo) else None,
                )
                if isinstance(sql_type, str):
                    break
            sql_type: str

            if isinstance(field_info, FieldInfo):
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
            else:
                migration_model.columns.append(Column(
                    name=column.name,
                    type_=sql_type,
                    attribute=Attribute(
                        null=is_null[0],
                    ),
                ))
        new_model.append(
            migration_model
        )
    return new_model


def get_old_model() -> List[MigrationsModel]:
    old_model: List[MigrationsModel] = []
    # create models
    return old_model


def migrations():
    new_models = get_new_model()
    old_models = get_old_model()
    sql_migrate: List[str] = []
    sql_rollback: List[str] = []

    for new_model in new_models:
        delete_old_model: Optional[MigrationsModel] = None
        for old_model in old_models:
            if new_model.name == old_model.name:
                delete_old_model = old_model

        if delete_old_model is None:
            sql_migrate.append(
                new_model.__sql_create_table__()
            )
            sql_rollback.append(
                new_model.__sql_drop_table__()
            )
        else:
            old_models.remove(delete_old_model)
            # alert __sql_alert_table__

    for old_model in old_models:
        sql_migrate.append(
            old_model.__sql_drop_table__()
        )
        sql_rollback.append(
            old_model.__sql_create_table__()
        )
    return sql_migrate, sql_rollback
