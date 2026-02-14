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
from Web.Feeds.Elements.Feed import Feed
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

        return ObjectsList(items = [String(value=text_value)])

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
        return ObjectsList(items = [String(value=i.get('text'))])

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
                    output = await response.text()
                except aiohttp.client_exceptions.ContentTypeError:
                    output = await response.text()
                    self.log_error(output)

        return ObjectsList(items = [String(value = output)])

class XML(Wheel):
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
            Argument(
                name = 'selector',
                orig = String,
                default = 'entry'
            ),
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        extract = self._get_submodule(i)

        assert extract != None, 'not found way'

        json = await extract.execute(i)
        output = json.items[0].value

        output_items = ObjectsList(items = [])

        parsed = Feed.parse(output)
        await self._set_items(i, parsed, output_items)

        return output_items

    async def _set_items(self, i: dict, xml: str, output: ObjectsList):
        import xmltodict

        selector = i.get('selector')
        _object = i.get('object')

        for item in xml.find_all(selector):
            try:
                _data = xmltodict.parse(str(item))
                got_item = await _object.from_xml(_data)
                output.append(got_item)
            except Exception as e:
                self.log_error(e, exception_prefix = 'Could not load object: ')
