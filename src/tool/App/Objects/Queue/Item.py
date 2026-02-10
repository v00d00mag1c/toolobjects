from App.Objects.Object import Object
from App import app
from pydantic import Field
from typing import Any
from App.Objects.Queue.LinkValue import LinkValue
from App.Objects.Queue.ValueWithReplaces import ValueWithReplaces
from App.Logger.LogPrefix import LogPrefix
from App.ACL.User import User

class Item(Object):
    '''
    Item of Queue.

    predicate: object that will be called
    constructor_arguments: dict with App.Objects.Queue.Argument values that will be used for constructor()
    arguments: dict with App.Objects.Queue.Argument values that calls execute()

    if you calling just an Object only constructor_arguments will be used
    '''
    predicate: str = Field()
    build: dict = Field(default = {})
    arguments: dict = Field(default = {})

    id: int = Field(default = None)

    def get_predicate(self):
        # i think predicate is a correct name?
        plugin = app.ObjectsList.getByName(self.predicate)
        if plugin == None:
            return None

        return plugin.getModule()

    def get_build_arguments(self, prestart: list, items: list):
        return self._get_arguments_from_dict(self.build, prestart, items)

    def get_arguments(self, prestart: list, items: list) -> dict:
        return self._get_arguments_from_dict(self.arguments, prestart, items)

    def _get_arguments_from_dict(self, from_dict: dict, prestart: list, items: list) -> dict:
        final_arguments = {}
        for key, val in from_dict.items():
            final_arguments[key] = self.getArgument(from_dict, key, val, prestart, items)

        return final_arguments

    def getArgument(self, original_arguments: dict, key: str, val: str | dict, prestart: list, items: list) -> Any:
        # Computing value
        if type(val) != dict:
            return val

        if 'direct_value' in val:
            vals = LinkValue(value = val.get('direct_value'))

            return vals.toString(prestart, items)

        if 'replacements' in val:
            vals = ValueWithReplaces(**val)

            return vals.toString(prestart, items)

    async def run(self, prestart: list, items: list, preexecutor: Object, auth: User):
        arguments = self.get_arguments(prestart, items)

        self.log(f"Running {self.predicate} with arguments {arguments}")

        item_class = self.get_predicate()
        item_instance = item_class(**self.get_build_arguments(prestart, items))

        arguments['i'] = item_instance
        arguments['auth'] = auth

        return await preexecutor.execute(arguments)

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(
            name = 'item',
            id = self.id
        )
