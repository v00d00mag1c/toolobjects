from App.Views.View import View
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Objects.Executable import Executable

class ConsoleView(View):
    async def implementation(self, i: dict = {}):
        print(i.get('i'))

    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            Executable(
                name = 'i',
                assertions = [
                    NotNoneAssertion()
                ]
            )
        ])
