from typing import TYPE_CHECKING, Iterator, List

if TYPE_CHECKING:
    from py_orm.sql_builder.read import Read, TModel, TSchema


def build_py_orm_model(value: 'Read[TModel, TSchema]', data: List[tuple]) -> Iterator['TSchema']:
    for column in data:
        virtual_data = {}
        for i, name in enumerate(value.columns):
            virtual_data[name] = column[i]
        yield value.schema_model(**virtual_data)
