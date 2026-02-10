from App.Objects.Arguments.ArgumentDict import ArgumentDict
from pydantic import Field

class Validable:
    '''
    Mixin that contains function with arguments lists that can be used for validation
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        '''
        Arguments for validation
        '''
        return ArgumentDict(items = [])

    @classmethod
    def getAllArguments(cls) -> ArgumentDict:
        '''
        Joins ArgumentDicts from all extended classes
        '''

        # Takes current ArgumentDict cuz it can contain properties
        _list = cls.getArguments()

        # Slicing 1 because first arguments already got
        for _class in cls.getMRO()[1:]:
            if hasattr(_class, 'getArguments') == True:
                new_arguments = _class.getArguments()
                if new_arguments == None:
                    continue

                _list.join(new_arguments)

        return _list
