from App.Objects.Object import Object
from pydantic import Field
from typing import Literal

class Permission(Object):
    type: Literal['object', 'item'] = Field()
    name: str = Field()
