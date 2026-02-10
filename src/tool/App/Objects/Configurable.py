from typing import Generator

class Configurable:
    '''
    Allows to define settings of Object (that are App.Arguments.Argument)
    '''

    @classmethod
    def getSettings(cls) -> list:
        pass

    @classmethod
    def getAllSettings(cls) -> Generator:
        alls = []

        for class_val in cls.meta.mro:
            if hasattr(class_val, "getSettings") == False:
                continue

            alls.append(class_val.getSettings())

        return alls
