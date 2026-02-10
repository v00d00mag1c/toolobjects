from App.Objects.Object import Object
from typing import Any as _Any

class Any(Object):
    @classmethod
    def asArgument(cls, val: _Any):
        return val
