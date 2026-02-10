from App.Objects.Mixins.BaseModel import BaseModel
from App.DB.Query.Values.Value import Value
from typing import Any, Optional
from pydantic import Field

class Condition(BaseModel):
    # so the condition has two parts: val (that compares) and val2 (that comparing with). both are Value but the same class has different fields
    val1: Value = Field()
    val2: Value = Field(default = None)
    operator: str | Any = Field(default = None)
    applied: bool = Field(default = False, exclude = True)

    def _get_any(self, val):
        if isinstance(val, Value):
            return val

    def getFirst(self):
        return self._get_any(self.val1)

    def getLast(self):
        return self._get_any(self.val2)
