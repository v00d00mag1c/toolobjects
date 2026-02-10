from App.Objects.Misc.DictList import DictList

class Variableable:
    '''
    Allows to define class variables. They will be created in every class instance.
    What they can do? maybe progressbar or preview result
    Variables are just DictList with App.Objects.Arguments.Argument. They are copying from prototype that already was inited
    '''
    _instance_variables: DictList | None = None

    def init_vars(self):
        # self.log('init vars')
        self._instance_variables = DictList(items = [])
        for var in self.__class__.getVariables():
            self._instance_variables.append(var)

    def trigger_variables(self):
        for var in self._instance_variables.toList():
            self.triggerHooks('var_update', variable = var)

    @classmethod
    def _variables(cls) -> list:
        pass

    @classmethod
    def getVariables(cls) -> list:
        alls = list()
        _names = list()

        for class_val in cls.getMRO():
            if hasattr(class_val, "_variables") == False:
                continue

            _vars = class_val._variables()
            if _vars == None:
                continue

            for var in _vars:
                if var.name in _names:
                    continue

                _new = var.model_copy()
                _new.autoApply()
                alls.append(_new)
                _names.append(_new.name)

        return alls
