#from App.Documentation.Documentation import Documentation
from .Assertions.Assertion import Assertion
from App.Objects.Object import Object
from typing import Any, List
from pydantic import Field, computed_field

class Argument(Object):
    name: str = Field()
    default: Any = Field(default = None)
    inputs: str = Field(default = None) # workaround
    is_sensitive: bool = Field(default = False)
    auto_apply: bool = Field(default = False)
    assertions: List[Assertion] = Field(default=[])

    current: Any = Field(default=None)

    # This is an abstract method.
    # I think it should pass self.inputs in i ? i={} as settings will not be used anyway
    def implementation(self, original_value: str) -> Any:
        return original_value

    def getValue(self, original_value: Any | str, sets_current: bool = True, *args, **kwargs) -> Any:
        result = self.implementation(original_value, *args, **kwargs)
        self.inputs = original_value

        if sets_current == True:
            self.current = result

        return result

    @computed_field
    @property
    def sensitive_default(self) -> Any:
        return self.default

    def checkAssertions(self):
        for assertion in self.assertions:
            assertion.check(self)

    def constructor(self):
        if self.auto_apply == True:
            self.autoApply()

    def autoApply(self):
        self.current = self.getValue()

    @property
    def not_passed_message(self):
        return 'not passed'

    @property
    def none_message(self):
        return 'returned None'
