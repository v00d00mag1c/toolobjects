from App.Objects.Submodule import Submodule

class Submodules:
    '''
    Allows to set objects that are connected with current object.
    It applies submodules by __mro__ and uses App.Objects.Submodule for linking

    Probaly "submodulable" but i wont change
    '''

    @classmethod
    def getSubmodules(cls) -> list[Submodule]:
        return []

    @classmethod
    def getAllSubmodules(cls) -> list[Submodule]:
        modules = []

        for item in cls.getMRO():
            if hasattr(item, 'getSubmodules') == False:
                continue

            _items = item.getSubmodules()
            if _items == None:
                continue

            for submodule in _items:
                modules.append(submodule)

        return modules
