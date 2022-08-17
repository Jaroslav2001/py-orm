from typing import (
    TYPE_CHECKING,
    TypedDict,
    Callable,
    Type,
    Union,
    Tuple,
    Generic,
    TypeVar,
    Optional,
)

if TYPE_CHECKING:
    from py_orm.migrations.migrations_model import MigrationsModel


TType = TypeVar('TType', bound=Type)


class ConvertType(Generic[TType]):
    type_: TType
    name_sql: str
    validator: Optional[
        Callable[
            [str, Union[int, Tuple[int, int], None]],
            str
        ]
    ]

    def __init__(
        self,
        type_: TType,
        name_sql: str,
        validator: Optional[
            Callable[
                [str, Union[int, Tuple[int, int], None]],
                str
            ]
        ] = None
    ):
        self.type_ = type_
        self.name_sql = name_sql
        self.validator = validator

    def type_python_to_sql(
            self,
            value: Type,
            length: Union[int, Tuple[int, int], None]
    ) -> Optional[str]:
        if issubclass(self.type_, value):
            if self.validator is None:
                if length is None:
                    return self.name_sql
                if isinstance(length, int):
                    return f'{self.name_sql}({length})'
                else:
                    return f'{self.name_sql}({length[0]}, {length[1]})'
            else:
                return self.validator(
                    self.name_sql,
                    length,
                )
        return None


class DialectSQL(TypedDict):
    list_table: str
    schema_table: str
    create_table: str
    alter_table: str
    drop_table: str
    schema_parsing: Callable[..., 'MigrationsModel']
    types: Tuple[
        ConvertType[int],
        ConvertType[float],
        ConvertType[str],
        ConvertType[bool],
        ConvertType[bytes],
    ]
    primary_key: str
    foreign_key: str
    unique: str
    index: str
    auto_increment: str
    not_null: str

