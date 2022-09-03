from typing import (
    Any,
    Optional,
    Union,
    TYPE_CHECKING,
    Tuple,
)

from pydantic.fields import Undefined
from pydantic.typing import NoArgAnyCallable

from .main import FieldInfo, OnActions

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny
    from py_orm.sql_builder.terms.sql import T_SQL


def Index(
    default: Any = Undefined,
    *,
    length: Union[int, Tuple[int, int], None] = None,
    primary_key: bool = False,
    auto_increment: bool = False,
    foreign_key: Optional[str] = None,
    on_delete: Optional[OnActions] = None,
    on_update: Optional[OnActions] = None,
    unique: bool = False,
    distinct: bool = False,
    query: Optional['T_SQL'] = None,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: str = None,
    title: str = None,
    description: str = None,
    exclude: Union['AbstractSetIntStr', 'MappingIntStrAny', Any] = None,
    include: Union['AbstractSetIntStr', 'MappingIntStrAny', Any] = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    max_digits: int = None,
    decimal_places: int = None,
    min_items: int = None,
    max_items: int = None,
    unique_items: bool = None,
    min_length: int = None,
    max_length: int = None,
    allow_mutation: bool = True,
    regex: str = None,
    discriminator: str = None,
    repr: bool = True,
    **extra: Any,
) -> Any:
    field_info = FieldInfo(
        default,
        length=length,

        primary_key=primary_key,
        auto_increment=auto_increment,

        foreign_key=foreign_key,
        on_delete=on_delete,
        on_update=on_update,

        unique=unique,
        index=True,

        distinct=distinct,
        query=query,

        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        **extra,
    )
    field_info._validate()
    return field_info
