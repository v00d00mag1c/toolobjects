from App.Objects.Wheel import Wheel
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Object import Object

class ExtendedWheel(Wheel):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            )
        ], missing_args_inclusion = True)

    def _wheel(self, i):
        _obj = i.get('object')
        modules = []
        for submodule in _obj.getSubmodules():
            if 'wheel' not in submodule.role and 'media_method' not in submodule.role:
                continue

            modules.append(submodule)

        _submodule = self.__class__.compareAndGetFirstSuitableSubmodule(modules, i)

        return _submodule
