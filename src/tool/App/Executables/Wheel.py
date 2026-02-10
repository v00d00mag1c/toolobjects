from App.Arguments.Comparer import Comparer
from App.Responses.Response import Response
from App.Objects.Executable import Executable
from App.Objects.Submodule import Submodule
from App.Arguments.ArgumentsDict import ArgumentsDict

class Wheel(Executable):
    '''
    Executable that chooses between extractors from submodules.
    Does not contains implementations and is just wheel between extractors with role=act
    firstly was names as Representation and that class was needed to represent an object
    '''

    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        itms = ArgumentsDict()
        itms.missing_args_inclusion = True

        return itms

    async def implementation_wrap(self, i) -> Response:
        '''
        Overrides the default Executable.Execute "implementation_wrap()" and allows for automatic extractor choosing
        You shouldn't override this. it's better to create single extractor
        '''

        modules = []
        for submodule in self.getAllSubmodules():
            if submodule.value != Submodule.ConnectionEnum.INTERNAL.value:
                continue

            if 'wheel' not in submodule.role:
                continue

            modules.append(submodule)

        _submodule = self.__class__.compareAndGetFirstSuitableSubmodule(modules, i)
        if _submodule == None:
            self.log("Suitable submodule not found, calling implementation()")

            return await self.implementation(i)

        self.log(f"Using submodule: {submodule.getClassNameJoined()}", section = ['Execute'])

        extract = _submodule.module()

        return await extract.execute(i)

    async def implementation(self, i):
        raise AssertionError("can't find suitable submodule")

    @classmethod
    def compareAndGetFirstSuitableSubmodule(cls, items: list, values: dict):
        '''
        Iterates got submodules (internal, role=wheel), calling comparer with each submodule, and if at least one (common?) arg is presented in dict, returning it
        '''
        for item in items:
            decl = Comparer(compare = item.module.getAllArguments(), values = values)

            if decl.diff():
                return item

        return None

    def _getOptimalStrategy(self):
        '''
        i dont rememba what strategy is
        '''
        pass
