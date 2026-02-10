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
    def getArguments(cls) -> ArgumentDict:
        '''
        Joins ArgumentDicts from all extended classes
        '''

        # Takes current ArgumentDict cuz it can contain properties
        _list = cls._arguments()

        # Slicing 1 because first arguments already got
        for _class in cls.getMRO()[1:]:
            if hasattr(_class, '_arguments') == True:
                new_arguments = _class._arguments()
                if new_arguments == None:
                    continue

                _list.join(new_arguments)

        return _list
