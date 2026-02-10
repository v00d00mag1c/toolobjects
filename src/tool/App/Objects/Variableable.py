from App.Data.DictList import DictList

class Variableable:
    '''
    Allows to define class variables. They will be created in every class instance.
    What they can do? maybe progressbar or preview result
    Variables are just DictList with App.Arguments.Argument. They are copying from prototype that already was inited
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

        for class_val in cls.getMRO():
            if hasattr(class_val, "getVariables") == False:
                continue
            _vars = class_val.getVariables()
            if _vars == None:
                continue

            for var in _vars:
                _new = var.copy()
                _new.autoApply()
                alls.append(_new)

        return alls
