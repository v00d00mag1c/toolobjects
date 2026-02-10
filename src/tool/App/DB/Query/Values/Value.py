from App.Objects.Mixins.BaseModel import BaseModel
from typing import Any
from pydantic import Field

class Value(BaseModel):
    column: str = Field(default = None)
    json_fields: list = Field(default = None)
    args: list = Field(default = None)
    value: Any = Field(default = None)
    func: str = Field(default = None)
