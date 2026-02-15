from App.Objects.Object import Object
from Web.Feeds.Protocols.RSS import RSS
from Web.Feeds.Protocols.Atom import Atom
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from App.Objects.Operations.Create.CreationItem import CreationItem

class Feed(Object):
    @classmethod
    async def download(cls, url: str) -> str:
        import aiohttp

        response_xml = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        return response_xml

    @classmethod
    def detect_type(cls, data):
        if data.find('rss'):
            return RSS

        if data.find('feed'):
            return Atom

    @classmethod
    def parse(self, data: str):
        _detect = EncodingDetector.find_declared_encoding(data, is_html=True)

        return BeautifulSoup(data.encode(_detect, errors = 'ignore'), 'xml')

    @classmethod
    def getArguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'download.thumbnails',
                orig = Boolean,
                default = True
            )
        ])

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'RSS Feed',
                object_name = 'Web.Feeds.Elements.Channel',
                create = 'Web.Feeds.Create'
            )
        ]
