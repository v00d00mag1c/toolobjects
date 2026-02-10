from App.Objects.Object import Object
from App.Arguments.Argument import Argument
from App.Data.DictList import DictList
# from App.Arguments.Comparer import Comparer
from pydantic import Field
from typing import Any

class ArgumentsDict(Object):
    '''
    Dict with arguments,
    [name]: [argument]
    Probaly needs to be refactored cuz of unknown behavior
    '''
    items: DictList | dict = Field(default= {})
    missing_args_inclusion: bool = Field(default = False)

    def add(self, name: str, argument: Argument):
        '''
        Appends new argument by name
        '''
        self.items[name] = argument

    def get(self, name: str, default: str | Any = None):
        '''
        Allows to get value (so it supposed to used as standart dict)
        '''
        _out = self.items.get(name)
        if _out == None:
            return default

        if getattr(_out, "value", None) != None:
            return _out.value
        else:
            return _out

    @staticmethod
    def fromList(items: list):
        '''
        Create ArgumentsDict from list of arguments
        '''
        return ArgumentsDict(items = DictList(items = items))

    def toNames(self) -> list:
        '''
        Return the names of arguments
        '''
        if hasattr(self.items, 'toNames'):
            return self.items.toNames()

        names = []
        for key, val in self.items.items():
            names.append(key)

        return names

    def toDict(self, exclude: list = []) -> dict:
        '''
        Returns the dict?
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
        
        from App.Arguments.Comparer import Comparer

        if check_arguments == True:
            _c = Comparer(
                compare = self,
                values = inputs,
                raise_on_assertions = raise_on_assertions,
                missing_args_inclusion = self.missing_args_inclusion
            )
            return _c.toDict()
        else:
            return ArgumentsDict(items = inputs)

    def join(self, another_dict) -> None:
        '''
        Appends another ArgumentsDict's items to current ArgumentsDict
        '''

        for item in another_dict.items:
            self.items.append(item)
