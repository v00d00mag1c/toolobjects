from App.Objects.Misc.Valueable import Valueable
from pydantic import Field

class Boolean(Valueable):
    value: bool = Field()

    @classmethod
    def asArgument(cls, val: int | str) -> bool:
        if val == None:
            return False

        return int(val) != 0
