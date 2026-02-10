from App.Executables.Extractor import Extractor
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Types.String import String
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

class XML(Extractor):
    @classmethod
    def getArguments(cls):
        return ArgumentsDict.fromList([
            String(
                name = 'xml',
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        pass
