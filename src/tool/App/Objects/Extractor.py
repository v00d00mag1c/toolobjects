from App.Objects.Executable import Executable
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Object import Object
from App.Objects.Arguments.Variable import Variable
from App.Objects.Relations.Link import Link
from App import app
from typing import Generator, ClassVar
import asyncio

class Extractor(Executable):
    '''
    Class that returns only ObjectsList
    '''

    self_name: ClassVar[str] = 'Extractor'

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

    def get_items(self) -> Generator[Object]:
        for item in self._instance_variables.get('items').value:
            yield item

    def set_total_count(self, count: int):
        self._instance_variables.get('items').value.total_count = count
        self.trigger_variables()

    async def _get_virtual_linked(self, with_role = None):
        _items = await self.execute(self.args)
        for item in _items.getItems():
            item.obj.is_tmp = True
            item.local_obj.make_public()
            item.flush(app.Storage.get(self.getDbName()))
            item.save()

            yield Link(
                item = item
            )

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
