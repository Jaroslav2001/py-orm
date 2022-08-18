from typing import TYPE_CHECKING, Iterator, List

if TYPE_CHECKING:
    from py_orm import TBaseModel, Read


def build_py_orm_model(value: 'Read[TBaseModel]', data: List[tuple]) -> Iterator['TBaseModel']:
    for column in data:
        virtual_data = {}
        for i, name in enumerate(value.columns):
            virtual_data[name] = column[i]
        yield value.model(**virtual_data)
