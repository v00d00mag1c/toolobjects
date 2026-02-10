from App.Data.DictList import DictList

class Variableable:
    '''
    Allows to define class variables. They will be created in every class instance.
    What they can do? maybe progressbar or result preview
    Variables are just list with App.Arguments.Argument
    '''
    variables: DictList = None

    def constructor(self):
        super().constructor()

        self.variables = DictList(items = [])
        for var in self.__class__.getAllVariables():
            self.variables.append(var)

    @classmethod
    def getVariables(cls) -> list:
        pass

    @classmethod
    def getAllVariables(cls) -> list:
        alls = []

        for class_val in cls.meta.mro:
            if hasattr(class_val, "getVariables") == False:
                continue
            _vars = class_val.getVariables()
            if _vars == None:
                continue

            for var in _vars:
                alls.append(var)

        return alls
