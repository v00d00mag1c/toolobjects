from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String

class AdvancedArgument(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'txt',
                orig = String(
                    min_length = 8,
                    max_length = 10
                ),
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        self.log('length of the string is nine characters')
