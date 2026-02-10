from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from App.Objects.Misc.DictList import DictList
from pydantic import Field
from typing import Any, Self, Optional

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
        Checks passed dict and runs it over every Argument's "_implementation()" and returns computed arguments
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

    def join(self, another_dict) -> Self:
        '''
        Appends another ArgumentDict's items to current ArgumentDict
        '''

        _names = self.toNames()

        for item in another_dict.items:
            if item.get_name_for_dictlist() in _names:
                # self.log('\"{0}\" is already exists'.format(item.get_name_for_dictlist()))
                continue

            self.items.append(item)

        return self

    def join_class(self, another_object: Object, only: Optional[list[str]] = None) -> Self:
        '''
        Appends arguments from another executable to current list.

        Arguments:
        "only": append only arguments with names that passed in that list.
        '''

        for item in another_object.getArguments().toList():
            if only != None and item.name not in only:
                continue

            self.items.append(item)

        return self
