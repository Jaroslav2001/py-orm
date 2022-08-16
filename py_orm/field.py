from typing import Any, Optional, Union, TYPE_CHECKING, Tuple

from pydantic.fields import FieldInfo as _FieldInfo, Undefined
from pydantic.typing import NoArgAnyCallable

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny


class FieldInfo(_FieldInfo):
    __slots__ = _FieldInfo.__slots__ + (
        'length',
        'primary_key',
        'foreign_key',
        'unique',
        'index',
        'auto_increment',
        'nullable',
    )

    def __init__(self, default: Any = Undefined, **kwargs: Any):
        self.length = kwargs.pop('length')
        self.auto_increment = kwargs.pop('auto_increment')
        self.primary_key = kwargs.pop('primary_key')
        self.foreign_key = kwargs.pop('foreign_key')
        self.unique = kwargs.pop('unique')
        self.index = kwargs.pop('index')
        self.nullable = None
        if self.primary_key:
            self.auto_increment = True
        super().__init__(default, **kwargs)


def Field(
    default: Any = Undefined,
    *,
    length: Union[int, Tuple[int, int], None] = None,
    primary_key: bool = False,
    foreign_key: bool = False,
    unique: bool = False,
    index: bool = False,
    auto_increment: bool = False,
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
        foreign_key=foreign_key,
        unique=unique,
        index=index,
        auto_increment=auto_increment,
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
