class Configurable:
    '''
    Allows to define settings of Object (that are App.Arguments.Argument)
    '''

    @classmethod
    def getSettings(cls) -> list:
        pass

    @classmethod
    def getAllSettings(cls):
        '''
        There are similar by code functions: Configurable.getAllSettings, Validable.getAllArguments, Submodules.getAllSubmodules, Variableable.getAllVariables.
        thats not so many, but it's better to move to MROThing or smth
        '''
        alls = []

        for class_val in cls.meta.mro:
            if hasattr(class_val, "getSettings") == False:
                continue

            item = class_val.getSettings()
            if item != None:
                alls.append(item)

        return alls
