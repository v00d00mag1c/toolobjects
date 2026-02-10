from App.Objects.Submodule import Submodule

class Submodules:
    '''
    Allows to set objects that are connected with current object.
    It applies submodules by __mro__ and uses App.Objects.Submodule for linking
    '''

    @classmethod
    def getSubmodules(cls) -> list[Submodule]:
        pass

    @classmethod
    def getAllSubmodules(cls) -> list[Submodule]:
        pass
