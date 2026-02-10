from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Act import Act

class String(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    def _display_as_string(self):
        return str(self.value)
