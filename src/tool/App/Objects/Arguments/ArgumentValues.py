from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Any

class ArgumentValues(Object):
    '''
    Class that imitates dictionary and comparer between object arguments and values
    '''

    compare: ArgumentDict = Field(default=None)
    values: dict = Field(default={})
    modified: bool = Field(default = False)

    raise_on_assertions: bool = Field(default=False)
    missing_args_inclusion: bool = Field(default=False)
    check_assertions: bool = Field(default=True)
    default_on_none: bool = Field(default=False)
    default_on_assertion: bool = Field(default=True)
    none_values_skipping: bool = Field(default=True)

    def set(self, key: str, val: Any) -> None:
        self.values[key] = val

    def toDict(self) -> dict:
        if self.compare == None:
            return self.values

        table = {}
        key_names = []
        if getattr(self.values, "toNames", None) != None:
            key_names = self.values.toNames()
        else:
            for name, val in self.values.items():
                key_names.append(name)

        for name in self.compare.toNames():
            key_names.append(name)

        for param_name in key_names:
            got_value = self.get(param_name)
            if got_value == None and self.none_values_skipping == True:
                continue

            table[param_name] = got_value

        return table

    def check(self) -> bool:
        '''
        check assertions or something
        '''

        self.toDict()

        return True

    def get(self, name: str, default: Any = None, same: bool = False):
        inputs = self.values.get(name)
        if same == True:
            return inputs

        if self.compare == None:
            return default

        argument: Argument = self.compare.get(name)
        if argument == None:
            if self.missing_args_inclusion == True:
                return inputs
            else:
                return default

        fallback = argument.sensitive_default

        value = argument.getValue(original_value = inputs)
        if value == None and self.default_on_none == True:
            value = fallback

        if self.check_assertions == True:
            try:
                argument.inputs = inputs
                argument.current = value
                argument.checkAssertions()
            except Exception as assertion:
                if self.raise_on_assertions == True:
                    raise assertion

                if self.default_on_assertion == True:
                    argument.current = fallback

        return value

    def diff(self):
        diff_value = 0

        for item_name in self.compare.toNames():
            if self.values.get(item_name) != None:
                #diff_value += 1
                return True

        return False

    def getValues(self, exclude: list[str]) -> dict:
        vals = dict()

        for key, val in self.values.items():
            if key in exclude:
                continue

            vals[key] = val

        return vals
