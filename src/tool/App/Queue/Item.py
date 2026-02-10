from App.Objects.Object import Object
from App import app
from pydantic import Field
from typing import Any
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Queue.LinkValue import LinkValue
from App.Queue.ValueWithReplaces import ValueWithReplaces
from App.Arguments.ArgumentsDict import ArgumentsDict

class Item(Object):
    '''
    Item of Queue.

    predicate: object that will be called
    constructor_arguments: dict with App.Queue.Argument values that will be used for constructor()
    arguments: dict with App.Queue.Argument values that calls execute()

    if you calling just an Object only constructor_arguments will be used
    '''
    predicate: str = Field()
    build: dict = Field(default = {})
    arguments: dict = Field(default = {})

    _queue: Any = None
    _id: int = None

    def getPredicate(self):
        plugin = app.app.objects.getByName(self.predicate)
        if plugin == None:
            return None

        return plugin.getModule()

    def getBuildArguments(self):
        return self.build

    def getArguments(self) -> dict:
        original_arguments = self.arguments
        final_arguments = {}

        for key, val in original_arguments.items():
            final_arguments[key] = self.getArgument(original_arguments, key, val)

        return ArgumentsDict(items = final_arguments)

    def getArgument(self, original_arguments: dict, key: str, val: str | dict) -> Any:
        # Computing value
        if type(val) != dict:
            return val

        if 'direct_value' in val:
            vals = LinkValue(value = val.get('direct_value'))

            return vals.toString(self._queue.prestart, self._queue.items)

        if 'replacements' in val:
            vals = ValueWithReplaces(**val)

            return vals.toString()

    async def run(self):
        arguments = self.getArguments()
        self.log(f"Running {self.predicate} with arguments {arguments.items}")

        item_class = self.getPredicate()
        item_instance = item_class(**self.getBuildArguments())

        return await item_instance.execute(arguments)

    @property
    def append_prefix(self): # -> LogPrefix
        return {'name': 'Item', 'id': self._id}
