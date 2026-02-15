from .Assertions.Assertion import Assertion
from App.Objects.Object import Object
from App.Objects.Misc.NameContainable import NameContainable
from App.Objects.Arguments.AllowedValues import AllowedValues
from typing import Any, List, Literal, Callable, Generator, Optional
from pydantic import Field, computed_field, field_serializer
from App.Locale.Documentation import Documentation
from App.Storage.StorageUUID import StorageUUID
from Data.Types.JSON import JSON
from App.Objects.Index.ModuleData import ModuleData
from App import app

class Argument(NameContainable):
    name: str = Field()
    orig: list[Any] | Any = Field(default = None, exclude = True)
    default: Any | Callable = Field(default = None)
    inputs: Any | str = Field(default = None) # workaround for assertions

    is_class_returns: bool = Field(default = False)
    is_sensitive: bool = Field(default = False)
    by_id: bool = Field(default = False)
    auto_apply: bool = Field(default = False)
    check_json: bool = Field(default = True)

    config_fallback: Optional[tuple[str, bool]] = Field(default = None) # list, 1 - name of the option, 2 - bool 0 - config 1 - env
    allowed_values: Optional[AllowedValues] = Field(default = None)

    assertions: List[Assertion] = Field(default=[])
    role: Literal['config', 'env'] = Field(default='config')
    documentation: Documentation = Field(default = None)
    serialization: Optional[dict] = Field(default = None)
    orig_serialization: Optional[dict] = Field(default = {
        'only_class_fields': True,
        'by_alias': True,
        'exclude_defaults': True,
    })

    current: Any = Field(default=None)

    # Messages

    not_passed_message: str = Field(default = '{0} not passed')
    none_message: str = Field(default = '{0} with value {1} is None')

    _unserializable = ['arg_value']

    def get_name_for_dictlist(self) -> str:
        return self.name

    def getValue(self, original_value: Any | str) -> Any:
        if original_value == None:
            _default = self.getDefault()
            if _default != None:
                original_value = _default

        if self.orig == None:
            return original_value

        return self.getImplementation(original_value)

    def getImplementation(self, original_value: Any | str):
        self.inputs = original_value

        if self.allowed_values != None:
            is_in = False

            if self.allowed_values.strict == True:
                for value in self.allowed_values.values:
                    if original_value == value:
                        is_in = True
            else:
                is_in = True

            assert is_in == True, '{0}: not allowed value {1}'.format(self.name, original_value)

        if self.check_json == True and JSON.isStringValidJson(original_value) == True:
            val = JSON.fromText(original_value).data

            return self._implementation(val)

        return self._implementation(original_value)

    def _implementation(self, val: Any | str) -> Any:
        _orig = self.getOrig()
        assert hasattr(_orig, 'asArgument'), 'orig item is not an object'

        if self.by_id == True:
            return self._by_id(val)

        if self.is_class_returns:
            return _orig.asClass(val)

        # If only class reference was passed in "orig"
        if callable(_orig):
            return _orig.asArgument(val)
        else:
            return _orig.asArgumentAsInstance(val)

    def _by_id(self, val: str):
        _orig = self.getOrig()
        if StorageUUID.validate(val):
            _val = StorageUUID.fromString(val).toPython()
            # for listargument
            if callable(_orig) == False:
                return _orig.asArgumentAsInstance(_val)

            return _val

    def getOrig(self) -> Object:
        return self.orig

    def getDefault(self):
        if self.config_fallback != None:
            if len(self.config_fallback) == 1:
                return app.Config.get(self.config_fallback[0])
            else:
                _where = 'config'
                if self.config_fallback[1] == True:
                    _where = 'env'

                return app.Config.get(self.config_fallback[0], role = _where)

        if callable(self.default):
            return self.default()
        else:
            return self.default

    @computed_field
    @property
    def sensitive_default(self) -> Any:
        return self.default

    @computed_field
    @property
    def arg_value(self) -> Any:
        '''
        Gets value from "inputs" field. Can be used in Queue.
        '''
        return self.getValue(self.inputs)

    def checkAssertions(self):
        for assertion in self.assertions:
            assertion.check(self)

    def init_hook(self):
        if self.auto_apply == True:
            self.autoApply()

    def serialize_self(self):
        return self.to_json(**self.serialization)

    def autoApply(self):
        self.current = self.getValue(None)

    @field_serializer('orig')
    def get_orig(self, orig) -> str:
        if orig == None:
            return None

        if callable(orig):
            _module = ModuleData.from_module(orig.__class__)
            _module.instance_values = orig.to_json(**self.orig_serialization)

            return _module
        else:
            return ModuleData.from_module(orig)

    def get_str_default(self):
        _str = self.get_default(self.default)
        if type(_str) == bool:
            _str = int(_str)

        if type(_str) == list:
            _str = JSON(data = _str).dump()

        return _str

    @field_serializer('default')
    def get_default(self, default) -> str:
        if callable(default) or self.is_sensitive or self.role == 'env':
            return None

        return default

    @field_serializer('inputs')
    def get_inputs(self, inputs) -> str:
        return None

    def set_input_value(self, value):
        self.inputs = value
