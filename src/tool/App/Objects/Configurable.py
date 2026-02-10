from App import app
from typing import Any, Literal

class Configurable:
    '''
    Allows to define settings of Object (that are App.Arguments.Argument)
    '''

    @classmethod
    def getSettings(cls) -> list:
        pass

    @classmethod
    def getAllSettings(cls, where: Literal['env', 'config'] = None):
        '''
        There are similar by code functions: Configurable.getAllSettings, Validable.getAllArguments, Submodulable.getAllSubmodules, Variableable.getAllVariables.
        thats not so many, but it's better to move to MROThing or smth
        '''
        alls = []

        for class_val in cls.getMRO():
            if hasattr(class_val, "getSettings") == False:
                continue

            items = class_val.getSettings()
            if items == None:
                continue

            for item in items:
                if where != None:
                    if where in item.role:
                        continue

                alls.append(item)

        return alls

    @classmethod
    def getAllEnvSettings(cls):
        return cls.getAllSettings(where='env')

    @classmethod
    def getOption(cls, name: str, default: Any = None, where: Literal['env', 'config'] = 'config'):
        return app.Config.get(name, default)
