from App.Objects.Executable import Executable
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Responses.ModelsResponse import ModelsResponse
from App.Objects.Object import Object
from App.Arguments.Objects.Orig import Orig

class Extractor(Executable):
    '''
    Class that doesn't needs to return anything. It just appends got items to variable
    '''

    @classmethod
    def getVariables(cls):
        from App.Arguments.Objects.List import List

        return [
            List(
                name = 'items',
                orig = Orig(
                    name = 'item',
                    object = Object
                ),
                default = []
            )
        ]

    def append(self, out: Object):
        '''
        Append to response
        '''
        self.variables.get("items").append(out)

    async def implementation(self, i = {}) -> None:
        '''
        not supposed to return something
        '''

        pass

    async def implementation_wrap(self, i = {}) -> ModelsResponse:
        await self.implementation(i)

        return ModelsResponse(models = self.variables.get("items").current)
