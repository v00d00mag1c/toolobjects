from App.Objects.Executable import Executable
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.Same import Same
from App.Objects.Saveable import Saveable
from App.Responses.ModelsResponse import ModelsResponse

class ObjectToSaveable(Executable):
    '''
    Flushes any object to ContentUnit
    '''

    @classmethod
    def getArguments(cls):
        return ArgumentsDict.fromList([
            Same(
                name = 'object'
            )
        ])

    async def implementation(self, i):
        obj = i.get('object')
        item = Saveable(**obj.to_json())

        return ModelsResponse(models=item)
