from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone

class Convertation(Executable):
    '''
    Executable that converts X model to Y model. Convertation logic needs to be writed in "_implementation()"
    '''

    @classmethod
    def getCommonObject(cls):
        return cls.getSubmodules(with_role=['object_in'])[0]

    @classmethod
    def getConvertsTo(cls):
        return cls.getSubmodules(with_role=['object_out'])[0]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = "orig",
                #orig = cls.getCommonObject(),
                # Unsolvable bug. getCommonObject() gets "Convertation" submodules and returns nothing. So you can pass everything here
                assertions = [
                    NotNone()
                ]
            )
        ])

    async def _implementation(self, i) -> ObjectsList:
        pass
