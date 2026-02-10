from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument

class Extractor(Executable):
    '''
    Class that returns only ObjectsList
    '''

    @classmethod
    def _variables(cls):
        return [
            Argument(
                name = 'items',
                default = ObjectsList(unsaveable = False)
            )
        ]

    def append(self, out: Object):
        self.variables.get("items").current.append(out)

    async def implementation(self, i = {}) -> None:
        '''
        Not supposed to return something.
        '''

        pass

    async def implementation_wrap(self, i = {}) -> ObjectsList:
        self.init_vars()

        await self.implementation(i)

        return self.variables.get("items").current
