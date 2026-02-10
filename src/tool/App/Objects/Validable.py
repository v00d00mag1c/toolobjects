from App.Arguments.ArgumentsDict import ArgumentsDict

class Validable:
    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        '''
        Arguments for validation
        '''
        return ArgumentsDict(items = {})

    @classmethod
    def getAllArguments(cls) -> ArgumentsDict:
        '''
        Joins ArgumentDicts from all extended classes
        '''

        # Takes current ArgumentsDict cuz it can contain properties
        _list = cls.getArguments()

        # Slicing 1 because first arguments already got
        for _class in cls.meta.mro[1:]:
            if hasattr(_class, 'getArguments') == True:
                new_arguments = _class.getArguments()
                if new_arguments == None:
                    continue

                _list.join(new_arguments)

        return _list
