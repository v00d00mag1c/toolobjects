from App.Objects.Executable import Executable
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Objects.Orig import Orig
from App.Logger.Log import Log

class PrintLog(Executable):
    @classmethod
    def getArguments(cls):
        return ArgumentsDict.fromList([
            Orig(
                name = 'log',
                orig = Log,
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        print(i.get('log').toStr())
