from App.Objects.Object import Object
from App import app
from pydantic import Field
from typing import Any
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

        return plugin.module

    def getBuildArguments(self):
        return self.build

    def getArguments(self):
        return self.arguments

    async def run(self):
        arguments = self.getArguments()
        self.log(f"Running {self.predicate} with arguments {arguments}")

        item_class = self.getPredicate()
        item_instance = item_class(**self.getBuildArguments())

        return await item_instance.execute(arguments)

    @property
    def append_prefix(self): # -> LogPrefix
        return {'name': 'Item', 'id': self._id}
