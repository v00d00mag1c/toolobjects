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
        # It must pass all arguments
        itms = ArgumentDict(items = [])
        itms.missing_args_inclusion = True

        return itms

    async def _implementation(self, i) -> Response:
        extract = self._get_submodule(i)
        if extract == None:
            self._suitable_not_found_message()

            return await self._not_found_implementation(i)

        return await extract.execute(i)

    async def _not_found_implementation(self, i):
        raise AssertionError("can't find suitable submodule")

    def _suitable_not_found_message(self):
        self.log("Suitable submodule not found, calling _not_found_implementation()")

    def _get_submodule(self, i):
        _submodule = self._wheel(i)
        if _submodule == None:
            return None

        extract = _submodule.item()

        self.log(f"Using submodule: {extract._getModuleName()}", section = ['Execute'])

        return extract

    def _wheel(self, i):
        modules = []
        for submodule in self.getSubmodules(check_repeats = False):
            if 'wheel' not in submodule.role:
                continue

            modules.append(submodule)

        if i.get('__wheel_select'):
            self.log('wheel is selected')
            for item in modules:
                if item.getItem()._getNameJoined() == i.get('__wheel_select'):
                    return item

        _submodule = self.__class__.compareAndGetFirstSuitableSubmodule(modules, i)
        if _submodule != None:
            return _submodule

    @classmethod
    def compareAndGetFirstSuitableSubmodule(cls, items: list, values: dict):
        '''
        Iterates got submodules (internal, role=wheel), calling comparer with each submodule, and if at least one (common?) arg is presented in dict, returning it
        '''

        _vals = list()

        max_index, max_value = 0, 0
        for item in items:
            decl = ArgumentValues(compare = item.getItem().getArguments(), values = values.getValues())
            _vals.append(decl.diff())

        # Find more compare values
        for id, item in enumerate(_vals):
            if item > max_value:
                max_index, max_value = id, item

        # If nothing found
        if max_value == 0:
            return None

        return items[max_index]
