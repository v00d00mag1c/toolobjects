from App.Objects.Mixins.BaseModel import BaseModel
from typing import Any, Optional
from pydantic import Field

class Condition(BaseModel):
    val1: Any = Field()
    val2: Any = Field(default = None)
    operator: str | Any = Field(default = None)
    sub: Optional[BaseModel] = Field(default = None) # sub condition
    json_fields: list = Field(default = None)
    applied: bool = Field(default = False, exclude = True)

    def getFirst(self):
        return self.val1

    def getLast(self):
        return self.val2
