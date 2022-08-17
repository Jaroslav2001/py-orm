from pydantic import BaseModel


class Attribute(BaseModel):
    primary_key: bool = False
    foreign_key: bool = False
    unique: bool = False
    index: bool = False
    auto_increment: bool = False
    null: bool = True
