from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Responses.Response import Response
from App.Objects.Executable import Executable
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Arguments.ArgumentDict import ArgumentDict

class Wheel(Executable):
    '''
    Executable that chooses between extractors from submodules.
    Does not contains implementations and is just wheel between extractors with role=act
    firstly was names as Representation and that class was needed to represent an object
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        itms = ArgumentDict(items = [])
        itms.missing_args_inclusion = True

        return itms

    async def implementation_wrap(self, i) -> Response:
        '''
        Overrides the default Executable.Execute "implementation_wrap()" and allows for automatic extractor choosing
        You shouldn't override this. it's better to create single extractor
        '''

        _submodule = self._wheel(i)
        if _submodule == None:
            self.log("Suitable submodule not found, calling implementation()")

            return await self.implementation(i)

        self.log(f"Using submodule: {_submodule.getClassNameJoined()}", section = ['Execute'])

        extract = _submodule.item()

        return await extract.execute(i)

    async def implementation(self, i):
        raise AssertionError("can't find suitable submodule")

    def _wheel(self, i):
        modules = []
        for submodule in self.getSubmodules():
            if 'wheel' not in submodule.role:
                continue

            modules.append(submodule)

        _submodule = self.__class__.compareAndGetFirstSuitableSubmodule(modules, i)
        if _submodule != None:
            return _submodule.item()

    @classmethod
    def compareAndGetFirstSuitableSubmodule(cls, items: list, values: dict):
        '''
        Iterates got submodules (internal, role=wheel), calling comparer with each submodule, and if at least one (common?) arg is presented in dict, returning it
        '''

        for item in items:
            decl = ArgumentValues(compare = item.item.getArguments(), values = values)
            if decl.diff():
                return item

        return None

    def _getOptimalStrategy(self):
        '''
        i dont rememba what strategy is
        '''
        pass
