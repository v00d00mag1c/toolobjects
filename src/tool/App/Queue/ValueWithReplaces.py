from App.Objects.Object import Object
from pydantic import Field

class ValueWithReplaces(Object):
    position: list[int, int] = None
    value: str = None

    def toString(self):
        pass
