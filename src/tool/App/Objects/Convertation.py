from App.Objects.Executable import Executable
from App.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

class Convertation(Executable):
    '''
    Executable that converts X model to Y model. Convertation logic needs to be writed in "implementation()"
    '''

    @classmethod
    def getCommonObject(cls):
        return cls.getAllSubmodules(with_role=['object_in'])[0]

    @classmethod
    def getConvertsTo(cls):
        return cls.getAllSubmodules(with_role=['object_out'])[0]

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items=[
            Argument(
                name = "orig",
                #orig = cls.getCommonObject(),
                # Unsolvable bug. getCommonObject() gets "Convertation" submodules and returns nothing. So you can pass everything here
                assertions = [
                    NotNoneAssertion()
                ]
            )
        ])

    async def implementation(self, i) -> ObjectsList:
        pass
