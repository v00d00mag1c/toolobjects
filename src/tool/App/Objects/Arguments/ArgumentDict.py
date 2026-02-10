from App.Objects.Arguments.Argument import Argument
from Data.DictList import DictList
from pydantic import Field
from typing import Any

class ArgumentDict(DictList):
    '''
    Dict with App.Objects.Arguments.Argument items
    '''

    missing_args_inclusion: bool = Field(default = False)

    def add(self, name: str, argument: Argument):
        '''
        Appends new argument by name
        '''

        self.items[name] = argument

    def get(self, name: str, default: str | Any = None) -> Any:
        '''
        Gets value (so it supposed to used as standart dict).

        This method can't be annotated, so no syntax highlight :(:(
        '''

        _out = super().get(name)
        if _out == None:
            return default

        if getattr(_out, "value", None) != None:
            return _out.value
        else:
            return _out

    def toDict(self, exclude: list = []) -> dict:
        '''
        Returns the dict
        '''
        _items = {}
        for name in self.toNames():
            if name in exclude:
                continue

            _items[name] = self.get(name)

        return _items

    def compareWith(self, inputs: dict, check_arguments: bool = True, raise_on_assertions: bool = True):
        '''
        Checks passed dict and runs it over every Argument's "implementation()" and returns computed arguments
        '''
        
        from App.Objects.Arguments.ArgumentValues import ArgumentValues

        if check_arguments == True:
            _c = ArgumentValues(
                compare = self,
                values = inputs,
                raise_on_assertions = raise_on_assertions,
                missing_args_inclusion = self.missing_args_inclusion
            )
            return _c
        else:
            return inputs

    def join(self, another_dict) -> None:
        '''
        Appends another ArgumentDict's items to current ArgumentDict
        '''

        # WORKAROUNDDD. do not write code when sleepy. I dont know why it returns as 
        _items = another_dict.items
        #if hasattr(_items, 'toList'):
        #    _items = _items.items

        for item in _items:
            self.items.append(item)
