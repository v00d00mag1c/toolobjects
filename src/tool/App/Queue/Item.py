from App.Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal, List
from App.Arguments.ArgumentsDict import ArgumentsDict

class Item(Object):
    predicate: str = Field()
    arguments: dict = Field(default = {})
