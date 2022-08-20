from typing import (
    TYPE_CHECKING,
    Callable,
    Type,
    Union,
    Tuple,
    Generic,
    TypeVar,
    Optional,
    Any,
    Dict,
)

from pydantic import BaseModel as _BaseModel, ValidationError
from pydantic.fields import ModelField

if TYPE_CHECKING:
    from py_orm.migrations.migrations_model import MigrationsModel


TType = TypeVar('TType', bound=Type)


class ConvertType(Generic[TType]):
    type_: TType
    name_sql: str
    validator_type: Optional[
        Callable[
            [str, Union[int, Tuple[int, int], None]],
            str
        ]
    ]
    validator_sql: Callable[[Any], str]
    validator_python: Callable[[Any], Any]

    def __init__(
        self,
        type_: TType,
        name_sql: str,
        validator_sql: Callable[[Any], str],
        validator_type: Optional[
            Callable[
                [str, Union[int, Tuple[int, int], None]],
                str
            ]
        ] = None
    ):
        self.type_ = type_
        self.name_sql = name_sql
        self.validator_sql = validator_sql
        self.validator_type = validator_type

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField):
        if not isinstance(v, cls):
            raise TypeError('Invalid value')
        if not field.sub_fields:
            return v
        if not(v.type_ is field.sub_fields[0].outer_type_):
            raise ValidationError
        return v

    def type_python_to_sql(
            self,
            value: Type,
            length: Union[int, Tuple[int, int], None]
    ) -> Optional[str]:
        if issubclass(self.type_, value):
            if self.validator_type is None:
                if length is None:
                    return self.name_sql
                if isinstance(length, int):
                    return f'{self.name_sql}({length})'
                else:
                    return f'{self.name_sql}({length[0]}, {length[1]})'
            else:
                return self.validator_type(
                    self.name_sql,
                    length,
                )
        return None

    def python_sql(self, __value: Any) -> str:
        return self.validator_sql(__value)


class TypesConvert(_BaseModel):
    __types__: Dict[Type, ConvertType] = {
        None: ConvertType(None, 'NULL', lambda x: 'NULL')
    }

    int: ConvertType[int]
    float: ConvertType[float]
    str: ConvertType[str]
    bool: ConvertType[bool]
    bytes: ConvertType[bytes]

    def __init__(self, **data: Any):
        super().__init__(**data)
        for __field in self.dict().values():
            __field: ConvertType
            self.__types__[__field.type_] = __field


class DialectSQL(_BaseModel):
    list_table: str
    schema_table: str
    create_table: str
    alter_table: str
    drop_table: str
    schema_parsing: Callable[..., 'MigrationsModel']
    types: TypesConvert
    primary_key: str
    foreign_key: str
    unique: str
    index: str
    auto_increment: str
    not_null: str
    null: str
