from .Assertion import Assertion
from ..Argument import Argument

class NotNoneAssertion(Assertion):
    def check(self, argument: Argument):
        if argument.default == None:
            assert argument.inputs != None, f"{argument.name} {argument.not_passed_message}"

        assert argument.current != None, f"{argument.name} with value {argument.inputs} {argument.none_message}"
