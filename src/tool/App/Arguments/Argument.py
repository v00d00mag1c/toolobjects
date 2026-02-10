#from App.Documentation.Documentation import Documentation
from .Assertions.Assertion import Assertion
from App.Objects.Object import Object
from typing import Any, List, Literal, Callable
from pydantic import Field, computed_field

class Argument(Object):
    '''
    Object that allows to define what arguments something (executable) uses.
    It takes string on input and can convert it to stated in name value.

    Example: App.Arguments.Objects.Executable takes string on input and returns the Plugin from list

    Passes in App.Data.DictList for convenience. So it relays on "name" field

    default: What value will be set if nothing passed
    assertions: List of App.Arguments.Assertions.*; post-getValue() checks. So it saves "inputs" and "current" for this
    current: what was got after "getValue()"
    auto_apply: current will be set after constructor()

    Argument can be used not only for validation, but for storing, for example, Queue "prestart"
    '''
    name: str = Field()
    default: Any | Callable = Field(default = None)
    inputs: str = Field(default = None) # workaround
    is_sensitive: bool = Field(default = False)
    auto_apply: bool = Field(default = False)
    assertions: List[Assertion] = Field(default=[])
    role: Literal['config', 'env'] = Field(default=[])

    current: Any = Field(default=None)

    def implementation(self, original_value: str) -> Any:
        '''
        Abstract method, must be overriden
        '''
        return original_value

    def getValue(self, original_value: Any | str, sets_current: bool = True, *args, **kwargs) -> Any:
        if original_value == None and self.default != None:
            original_value = self.getDefault()

        result = self.implementation(original_value, *args, **kwargs)
        self.inputs = original_value
        if sets_current == True:
            self.current = result

        return result

    def getDefault(self):
        if callable(self.default):
            return self.default()
        else:
            return self.default

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
        self.current = self.getValue(None)

    @property
    def not_passed_message(self):
        return 'not passed'

    @property
    def none_message(self):
        return 'returned None'
