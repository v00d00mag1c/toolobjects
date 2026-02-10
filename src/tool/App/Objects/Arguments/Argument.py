from .Assertions.Assertion import Assertion
from App.Objects.Object import Object
from App.Objects.Misc.NameContainable import NameContainable
from typing import Any, List, Literal, Callable, Generator
from pydantic import Field, computed_field, field_serializer
from App.Locale.Documentation import Documentation
from App.Storage.StorageUUID import StorageUUID
from Data.Types.JSON import JSON
from App.Objects.Index.ModuleData import ModuleData

class Argument(NameContainable):
    name: str = Field()
    orig: list[Any] | Any = Field(default = None)
    default: Any | Callable = Field(default = None)
    inputs: str = Field(default = None) # workaround for assertions

    literally: bool = Field(default = False)
    is_sensitive: bool = Field(default = False)
    by_id: bool = Field(default = False) # workaround + hardcode
    auto_apply: bool = Field(default = False)
    check_json: bool = Field(default = True)

    assertions: List[Assertion] = Field(default=[])
    role: Literal['config', 'env'] = Field(default='config')
    documentation: Documentation = Field(default = None)

    current: Any = Field(default=None)

    # Messages

    not_passed_message: str = Field(default = '{0} not passed')
    none_message: str = Field(default = '{0} with value {1} is None')

    def get_name_for_dictlist(self) -> str:
        return self.name

    def getValue(self, original_value: Any | str) -> Any:
        if original_value == None and self.default != None:
            original_value = self.getDefault()

        if self.orig == None:
            return original_value

        return self.getImplementation(original_value)

    def getImplementation(self, original_value: Any | str):
        self.inputs = original_value

        if self.check_json == True and JSON.isStringValidJson(original_value) == True:
            val = JSON.fromText(original_value).data

            return self._implementation(val)

        return self._implementation(original_value)

    def _implementation(self, val: Any | str) -> Any:
        if self.by_id == True:
            if StorageUUID.validate(val):
                return StorageUUID.fromString(val).toPython()

        if self.literally:
            return self.getOrig().asClass(val)

        return self.getOrig().asArgument(val)

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

    def init_hook(self):
        if self.auto_apply == True:
            self.autoApply()

    def autoApply(self):
        self.current = self.getValue(None)

    @field_serializer('orig')
    def get_orig(self, orig) -> str:
        if orig == None:
            return None

        return ModuleData.from_module(orig)

    @field_serializer('default')
    def get_default(self, default) -> str:
        if callable(default) or self.is_sensitive or self.role == 'env':
            return None

        return default

    @field_serializer('inputs')
    def get_inputs(self, inputs) -> str:
        return None
