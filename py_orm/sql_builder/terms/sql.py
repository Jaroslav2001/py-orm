from typing import TypeVar
from abc import abstractmethod, ABC


class SQL(ABC):
    @property
    @abstractmethod
    def __sql__(self) -> str:
        ...

    def __str__(self) -> str:
        return self.__sql__


T_SQL = TypeVar('T_SQL', bound=SQL)
