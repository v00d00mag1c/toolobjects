from App.Objects.Act import Act
from App.Objects.Wheel import Wheel
from App.Objects.Object import Object
from App.Objects.Misc.Abstract import Abstract
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Relations.Submodule import Submodule
from Data.Types.String import String
from Data.Types.JSON import JSON as JSONObject
from pathlib import Path

class FromFile(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'file',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'encoding',
                orig = String,
                default = 'utf-8'
            )
        ])

    async def _implementation(self, i):
        assert self.getOption('app.permissions.file_access') == True, 'access denied'

        encoding = i.get('encoding')
        file = Path(i.get('file'))
        text_value = file.read_text(encoding = encoding)

        return ObjectsList(items = [JSONObject.fromText(text_value)])

class FromText(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'text',
                orig = String,
                assertions = [NotNone()]
            ),
        ])

    async def _implementation(self, i):
        return ObjectsList(items = [JSONObject.fromText(i.get('text'))])

class FromURL(Act):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
        ])

    async def _implementation(self, i):
        import aiohttp

        _end_url = i.get('url')
        output = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(_end_url) as response:
                try:
                    output = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    output = await response.text()
                    self.log_error(output)

        return ObjectsList(items = [JSONObject(data = output)])

class JSON(Wheel):
    @classmethod
    def _submodules(cls):
        return [
            Submodule(
                item = FromFile,
                role = ['wheel']
            ),
            Submodule(
                item = FromText,
                role = ['wheel']
            ),
            Submodule(
                item = FromURL,
                role = ['wheel']
            ),
        ]

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                default = 'App.Objects.Misc.Abstract'
            ),
            ListArgument(
                name = 'count_key',
                orig = String,
            ),
            ListArgument(
                name = 'items_key',
                orig = String
            ),
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        _object = i.get('object')
        extract = self._get_submodule(i)

        assert extract != None, 'not found way'

        json = await extract.execute(i)
        output = json.items[0].data
        output_items = ObjectsList(items = [])

        count = output
        items = output

        def _iterate_val(data):
            for item, key in data.items():
                if type(key) == dict:
                    yield from _iterate_val(key)
                else:
                    yield item, key

        if len(i.get('count_key')) > 0:
            for key in i.get('count_key'):
                count = count[key]
        else:
            self.log('You haven\'t passed count_key, trying to guess it.')

            for key, item in _iterate_val(count):
                if type(item) == int:
                    count = item
                    break

        if len(i.get('items_key')) > 0:
            for key in i.get('items_key'):
                items = items[key]
        else:
            self.log('You haven\'t passed items_key, trying to guess it.')

            for key, item in _iterate_val(items):
                if type(item) == list:
                    items = item
                    break

        assert items != None, 'not found items, probaly error or wrong items_key'

        if count != None and type(count) == int:
            output_items.set_total_count(count)

        for item in items:
            try:
                got_item = await _object.from_some_api(item)
                output_items.append(got_item)
            except Exception as e:
                self.log_error(e, exception_prefix = 'Could not load object: ')

        return output_items
