from App.Objects.Misc.Valueable import Valueable
from App.Objects.Act import Act

class Int(Valueable):
    # It should be named "Integer"
    value: int = None

    def _display_as_string(self):
        return str(self.value)

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return int(val)
