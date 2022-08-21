from typing import TypeVar, Type, List, Iterator, Tuple

from pydantic import BaseModel as _BaseModel

from dialect import dialect
from py_orm import TBaseModel, BaseModel, Create, CreateOne, Read


class BaseManager(_BaseModel):
    def create_one(self, __qwery: QwerySQL[CreateOne[TBaseModel]], __value: TBaseModel):
        __result = self._build_py_sql(**__value.dict())
        self.execute(__qwery.__sql__.format(
            *__result[0], **__result[1],
        ))

    def create_all(self, __qwery: QwerySQL[Create[TBaseModel]], *args: TBaseModel):
        self.execute(__qwery.__sql__.format([]))

    def read_all(
            self,
            __qwery: QwerySQL[Read[TBaseModel]],
            *args,
            **kwargs
    ) -> Iterator[TBaseModel]:
        print(args, kwargs)
        args, kwargs = self._build_py_sql(*args, **kwargs)
        print(args, kwargs)
        print(__qwery.__sql__.format(*args, **kwargs))
        self.execute(__qwery.__sql__.format(*args, **kwargs))
        return self._build_py_orm_model(value=__qwery.__qwery__.model, data=self.fetchall())


TBaseManager = TypeVar('TBaseManager', bound=BaseManager)
