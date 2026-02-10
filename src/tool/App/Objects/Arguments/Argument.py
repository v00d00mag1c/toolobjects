#from App.Documentation.Documentation import Documentation
from .Assertions.Assertion import Assertion
from App.Objects.Object import Object
from typing import Any, List, Literal, Callable, Generator
from pydantic import Field, computed_field
from App.Objects.Locale.Documentation import Documentation
from Data.JSON import JSON

class Argument(Object):
    '''
    Object that allows to define what arguments something (executable) uses.
    It takes string on input and can convert it to stated in name value.

    Passes in App.Data.DictList for convenience. So it relays on "name" field

    default: What value will be set if nothing passed
    assertions: List of App.Objects.Arguments.Assertions.*; post-getValue() checks. So it saves "inputs" and "current" for this
    current: what was got after "getValue()"
    auto_apply: current will be set after constructor()

    Argument can be used not only for validation, but for storing, for example, Queue "prestart"
    '''

    name: str = Field()
    orig: Any = Field()
    default: Any | Callable = Field(default = None)
    inputs: str = Field(default = None) # workaround
    is_multiple: bool = Field(default = False)
    is_sensitive: bool = Field(default = False)
    auto_apply: bool = Field(default = False)
    assertions: List[Assertion] = Field(default=[])
    role: Literal['config', 'env'] = Field(default=[])
    documentation: Documentation = Field(default = None)

    current: Any = Field(default=None)

    def getValue(self, original_value: Any | str) -> Any:
        result = None
        if original_value == None and self.default != None:
            original_value = self.getDefault()

        if self.orig == None:
            return original_value

        if self.is_multiple == True:
            result = list(self.getListValue(original_value))
        else:
            result = self.getOrig().asArgument(original_value)

        return result

    def getListValue(self, original_value: str | list) -> Generator[Any]:
        if type(original_value) == str:
            if JSON.isStringValidJson(original_value) == True:
                original_value = JSON.fromText(original_value).data
            else:
                if self.allow_commas_fallback:
                    original_value = original_value.split(',')

        if original_value == None:
            return None

        for item in original_value:
            yield self.getOrig().asArgument(val = item)

    def getOrig(self) -> Object:
        return self.orig

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
