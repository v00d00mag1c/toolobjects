from App.Objects.Misc.Valueable import Valueable
from typing import Any as _Any

class Any(Valueable):
    @classmethod
    def asArgument(cls, val: _Any):
        return val
