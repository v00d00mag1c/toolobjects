from App.Objects.Relations.Submodule import Submodule

class Submodulable:
    '''
    Allows to set objects that are connected with current object.
    It applies App.Objects.Submodules from __mro__
    '''

    @classmethod
    def _submodules(cls) -> list[Submodule]:
        return []

    @classmethod
    def getSubmodules(cls, with_role: list[str] | None = None) -> list[Submodule]:
        modules = []
        _names = list()

        for item in cls.getMRO():
            if hasattr(item, '_submodules') == False:
                continue

            _items = item._submodules()
            if _items == None:
                continue

            for submodule in _items:
                if submodule.item._getNameJoined() in _names:
                    continue

                if with_role != None:
                    contains_len = 0
                    for role in submodule.role:
                        if role in with_role:
                            contains_len += 1

                    if contains_len < len(with_role):
                        continue

                modules.append(submodule)
                _names.append(submodule.item._getNameJoined())

        return modules
