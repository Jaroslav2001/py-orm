from typing import (
    Set,
)

from typing_extensions import (
    Self,
)


class TableField:
    primary_key_: Set[str]
    auto_increment_: Set[str]

    unique_: Set[str]
    index_: Set[str]

    def __init__(self):
        self.primary_key_ = set()
        self.auto_increment_ = set()
        self.unique_ = set()
        self.index_ = set()

    def primary_key(self, *args: str) -> Self:
        self.primary_key_.update(args)
        return self

    def auto_increment(self, *args: str) -> Self:
        self.auto_increment_.update(args)
        return self

    def unique(self, *args: str) -> Self:
        self.unique_.update(args)
        return self

    def index(self, *args: str) -> Self:
        self.index_.update(args)
        return self
