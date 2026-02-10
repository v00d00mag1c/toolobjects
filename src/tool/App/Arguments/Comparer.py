from App.Objects.Object import Object
from App.Data.DictList import DictList
from App.Arguments.ArgumentsDict import ArgumentsDict
from .Argument import Argument
from pydantic import Field
from App import app

class Comparer(Object):
    '''
    Runs every Argument with raw value and returns dict with result
    '''

    compare: ArgumentsDict = Field(default=None)
    values: dict | ArgumentsDict = Field(default={})

    raise_on_assertions: bool = Field(default=False)
    missing_args_inclusion: bool = Field(default=False)
    default_on_none: bool = Field(default=False)
    default_on_assertion: bool = Field(default=True)
    none_values_skipping: bool = Field(default=True)

    def toDict(self) -> ArgumentsDict:
        if self.compare == None:
            return self.values

        # app.Logger.log(f"comparing {self.compare} and {self.values}", section=["Comparer", "ComparingArrays"])

        table = ArgumentsDict()
        key_names = []

        if getattr(self.values, "toNames", None) != None:
            key_names = self.values.toNames()
        else:
            for name, val in self.values.items():
                key_names.append(name)

        for name in self.compare.toNames():
            key_names.append(name)

        for param_name in key_names:
            got_value = self.getByName(param_name, missing_args_inclusion = self.missing_args_inclusion)

            if got_value == None and self.none_values_skipping == True:
                continue

            table.add(param_name, got_value)

        return table

    def getByName(self, name, check_assertions: bool = True, missing_args_inclusion: bool = False):
        inputs = self.values.get(name)
        argument: Argument = self.compare.get(name)

        if argument == None:
            if missing_args_inclusion == True:
                return inputs
            else:
                return None

        fallback = argument.sensitive_default
        value = argument.getValue(original_value = inputs, sets_current = True)

        if value == None and self.default_on_none == True:
            value = fallback

        if check_assertions == True:
            try:
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
