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
    def _get_submodule_by_last(cls, name: str, with_role: list[str] = None):
        for module in cls.getSubmodules(with_role = with_role):
            if module.getItem()._getModuleName() == name:
                return module.getItem()

    # why not generator?
    @classmethod
    def getSubmodules(cls, check_repeats: bool = True, with_role: list[str] | None = None) -> list[Submodule]:
        modules = []
        _names = list()

        for item in cls.getMRO():
            if hasattr(item, '_submodules') == False:
                continue

            _items = item._submodules()
            if _items == None:
                continue

            for submodule in _items:
                if check_repeats and submodule.getItem()._getNameJoined() in _names:
                    continue

                if with_role != None:
                    contains_len = 0
                    for role in submodule.role:
                        if role in with_role:
                            contains_len += 1

                    if contains_len < len(with_role):
                        continue

                modules.append(submodule)
                _names.append(submodule.getItem()._getNameJoined())

        return modules
