from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Object import Object
from App.Objects.Arguments.Variable import Variable
import asyncio

class Extractor(Executable):
    '''
    Class that returns only ObjectsList
    '''

    @classmethod
    def _variables(cls):
        return [
            Variable(
                name = 'items',
                value = ObjectsList(unsaveable = False),
                serialization = {
                    'exclude': ['items']
                }
            )
        ]

    @classmethod
    def getClassEventTypes(cls):
        return super().getClassEventTypes() + ['var_update']

    def append(self, out: Object):
        self._instance_variables.get('items').value.append(out)
        self.trigger_variables()

    def set_total_count(self, count: int):
        self._instance_variables.get('items').value.total_count = count
        self.trigger_variables()

    async def _implementation(self, i = {}) -> None:
        '''
        Not supposed to return something.
        '''

        pass

    async def implementation_wrap(self, i = {}) -> ObjectsList:
        self.init_vars()

        if asyncio.iscoroutinefunction(self._implementation):
            await self._implementation(i)
        else:
            self._implementation(i)

        return self._instance_variables.get("items").value
