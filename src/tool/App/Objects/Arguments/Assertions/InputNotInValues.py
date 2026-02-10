from .Assertion import Assertion
from ..Argument import Argument
from pydantic import Field

class InputNotInValues(Assertion):
    values: list = Field()

    def check(self, argument: Argument):
        assert argument.inputs not in self.values, f"{argument.name}: forbidden value"
