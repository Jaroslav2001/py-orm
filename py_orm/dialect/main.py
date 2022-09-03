from typing import (
    Dict,
)

from typing_extensions import (
    TypeAlias,
    Literal,
    Type,
)

from .abstract import TDialectAbstract
from .sqlite import Sqlite

DialectType: TypeAlias = Literal['sqlite', 'mysql', 'postgresql']

dialect: Dict[DialectType, Type[TDialectAbstract]] = {
    'sqlite': Sqlite,
}
