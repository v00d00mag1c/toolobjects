from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from App.Objects.Threads.ExecutionThread import ExecutionThread
from App.Objects.Autostart.Item import Item
from Data.Types.Boolean import Boolean
from typing import Any
from pydantic import Field
from App import app

class List(Object):
    items: list[Item] = Field(default = [])
    _pre_i: Any = None

    @classmethod
    def mount(cls):
        autostarts = cls(
            items = []
        )

        for item in cls.getOption('app.autostart.items'):
            autostarts.items.append(item)

        app.mount('Autostart', autostarts)

    async def run_by_dict(self, val: dict):
        _item = Item.model_validate(val)
        if _item.deactivated == True:
            return

        await self.start_item(_item, iterator = -3)

    async def start_them(self, pre_i):
        self.log('Starting startup scripts')

        _iterator = 0

        self._pre_i = pre_i()

        for item in self.items:
            if item.deactivated:
                continue

            await self.start_item(item, _iterator)
            _iterator += 1

    async def start_item(self, item, iterator):
        as_root = self.getOption('app.autostart.as_root')

        try:
            item.run(self._pre_i, 'autostart_item ' + str(iterator), as_root)

        except Exception as e:
            self.log_error(e)

            item.end()

    @classmethod
    def _settings(cls):
        return [
            Argument(
                name = 'app.autostart.as_root',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'app.scheduled_tasks.as_root',
                default = False,
                orig = Boolean
            ),
            ListArgument(
                name = 'app.autostart.items',
                default = [],
                orig = Item,
            )
        ]
