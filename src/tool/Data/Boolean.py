from App.Objects.Object import Object
from pydantic import Field

class Boolean(Object):
    value: bool = Field()

    @classmethod
    def asArgument(cls, val: int | str) -> bool:
        if val == None:
            return False

        return int(val) != 0
