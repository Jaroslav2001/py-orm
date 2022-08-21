from typing import Tuple, Union, List, Dict
import re

from pypika.terms import ValueWrapper

from py_orm import TBaseModel


class SQLReqwest(str):
    async def __call__(self, *args, **kwargs):
        ...

    @staticmethod
    def _value_wrapper(__value) -> str:
        return str(ValueWrapper(__value))

    @staticmethod
    def _values_wrapper(*args, **kwargs) -> Tuple[List[str], Dict[str, str]]:
        args = list(args)

        for i, j in enumerate(args):
            args[i] = str(ValueWrapper(j))

        for i, j in kwargs.items():
            kwargs[i] = str(ValueWrapper(j))

        return args, kwargs

    def insert_sql(self, *args, **kwargs) -> str:
        __re = re.search(r"\(\$([\w\s{}]*)\)", self)

        if __re is None:
            args, kwargs = self._values_wrapper(*args, **kwargs)
            # not NULL support auto
            return self.format(*args, **kwargs)

        else:
            __t = f"({', '.join(__re.groups()[0].split(' '))})"
            args: List[Union[dict, TBaseModel]]
            __result: List[str] = []
            for __value in args:
                _, __value = self._values_wrapper(**dict(__value))

                __result.append(
                    __t.format(**__value)
                )
            return re.sub(
                r"\(\$([\w\s{}]*)\)",
                ', '.join(__result),
                self,
            )
