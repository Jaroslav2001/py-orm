from typing import List, Optional

from pydantic.fields import ModelField

from py_orm import BaseModel, TBaseModel
from py_orm.main import is_type
from py_orm.dialect import dialect
from py_orm.field import FieldInfo

from .. import SQLBuilder
from . import Attribute, Column, MigrationsModel


class Database(SQLBuilder):
    _new_model: List[MigrationsModel]
    _old_model: List[MigrationsModel]
    _sql_command: List[str]

    def __init__(self):
        self.get_new_models()
        self.get_old_models()
        self.migrations()

    def __sql__(self) -> str:
        return '\n\n'.join(self._sql_command)

    @staticmethod
    def __sql__commit__(__migrate: str, __rollback: str) -> str:
        return f"-- <start>\n" \
               f"-- migrate\n" \
               f"{__migrate}\n" \
               f"-- rollback\n" \
               f"{__rollback}\n" \
               f"-- <end>\n"

    def migrations(self):
        self._sql_command = []

        for new_model in self._new_model:
            delete_old_model: Optional[MigrationsModel] = None
            for old_model in self._old_model:
                if new_model.name == old_model.name:
                    delete_old_model = old_model

            if delete_old_model is None:
                self._sql_command.append(
                    self.__sql__commit__(
                        new_model.__sql_create_table__(),
                        new_model.__sql_drop_table__(),
                    )
                )
            else:
                self._old_model.remove(delete_old_model)
                # alert __sql_alert_table__

        for old_model in self._old_model:
            self._sql_command.append(
                self.__sql__commit__(
                    old_model.__sql_drop_table__(),
                    old_model.__sql_create_table__(),
                )
            )

    def get_new_models(self) -> List[MigrationsModel]:
        self._new_model = []
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
                        if not (i is None):
                            type_ = i
                elif len(is_null[1]) == 0:
                    type_ = is_null[2]

                # get sql type
                field_info: FieldInfo = column.field_info
                sql_type: str = ''

                for i in dialect[BaseModel.__config_py_orm__.dialect].types.__types__.values():
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
                        length=None,
                        attribute=Attribute(
                            null=is_null[0],
                        ),
                    ))
            self._new_model.append(
                migration_model
            )
        return self._new_model

    def get_old_models(self):
        self._old_model = []
        # create models
