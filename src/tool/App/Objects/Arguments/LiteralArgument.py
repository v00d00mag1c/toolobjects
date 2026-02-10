from App.Objects.Arguments.Argument import Argument
from pydantic import Field

class LiteralArgument(Argument):
    values: list = Field(default = [])
    strict: bool = Field(default = True)
    
    def implementation(self, val: str):
        is_in = False

        if self.strict == True:
            for value in self.values:
                if val == value:
                    is_in = True
        else:
            is_in = True

        assert is_in == True, "not allowed value"

        return val
