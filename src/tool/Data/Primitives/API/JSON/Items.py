from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Misc.Abstract import Abstract
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.String import String

class Items(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
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
        ])

    async def _implementation(self, i):
        import aiohttp

        _object = i.get('object')
        _end_url = i.get('url')
        output = None

        async with aiohttp.ClientSession() as session:
            async with session.get(_end_url) as response:
                try:
                    output = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    self.log_error(await response.text())

        count = output
        items = output
        for key in i.get('count_key'):
            count = count[key]
        for key in i.get('items_key'):
            items = items[key]
 
        assert items != None, 'not found items. maybe wrong items_key?'

        if count != None and type(count) == int:
            self.set_total_count(count)

        for item in items:
            try:
                got_item = await _object.from_some_api(item)
                self.append(got_item)
            except Exception as e:
                self.log_error(e, exception_prefix = 'Could not load object: ')
