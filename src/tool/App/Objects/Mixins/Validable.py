from App.Objects.Arguments.ArgumentDict import ArgumentDict
from pydantic import Field

class Validable:
    '''
    Mixin that contains function with arguments lists that can be used for validation
    '''

    def getCompareKeys(self) -> list:
        _keys = list()
        for item in self.getArguments().toList():
            _keys.append(item.name)

        return _keys

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        '''
        Arguments for validation
        '''
        return ArgumentDict(items = [])

    @classmethod
    def getArguments(cls, include_usage: bool = False) -> ArgumentDict:
        '''
        Joins ArgumentDicts from all extended classes
        '''

        # Takes current ArgumentDict
        _list = cls._arguments()

        # Slicing the current ArgumentDict
        for _class in cls.getMRO()[1:]:
            if hasattr(_class, '_arguments'):
                new_arguments = _class._arguments()
                if new_arguments == None:
                    continue

                _list.join(new_arguments)

        if include_usage == True:
            for submodule in cls.getSubmodules(with_role = ['usage']):
                _list.join(submodule.getArguments())

        return _list
