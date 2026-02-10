from App.Objects.Object import Object
from typing import Any
from pydantic import Field

class Valueable(Object):
    value: Any = Field(default = None)
