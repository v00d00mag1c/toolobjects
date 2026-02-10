from App.Objects.BaseModel import BaseModel
from typing import Any
from pydantic import Field

class Condition(BaseModel):
    val1: Any = Field()
    operator: str | Any = Field()
    val2: Any = Field()
    json_fields: str = Field(default = None)

    def getFirst(self):
        return self.val1

    def getLast(self):
        return self.val2
